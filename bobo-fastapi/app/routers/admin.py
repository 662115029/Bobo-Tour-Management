from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from app.db.connection import get_connection, get_cursor
import bcrypt

router = APIRouter(prefix="/admin", tags=["admin"])


class LoginRequest(BaseModel):
    username: str
    password: str


class LogRequest(BaseModel):
    admin_id: str
    action_type: str
    target_type: str
    target_id: str
    target_name: str
    note: Optional[str] = None


@router.get("/db/ping")
def admin_db_ping():
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute("SELECT 1 AS ok")
        row = cursor.fetchone()
        conn.close()
        return {"db": "mysql", "connected": True, "ok": row["ok"]}
    except Exception as e:
        return {"db": "mysql", "connected": False, "error": str(e)}


@router.get("/stats")
def admin_stats():
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute("SELECT COUNT(*) AS c FROM jobs")
        totalJobs = int(cursor.fetchone()["c"])
        cursor.execute("SELECT COUNT(*) AS c FROM employers")
        total_employers = int(cursor.fetchone()["c"])
        cursor.execute("SELECT COUNT(*) AS c FROM freelancers")
        total_freelancers = int(cursor.fetchone()["c"])
        cursor.execute("SELECT COUNT(*) AS c FROM employers WHERE em_verify_status = 'PENDING'")
        pending_employers = int(cursor.fetchone()["c"])
        cursor.execute("SELECT COUNT(*) AS c FROM freelancers WHERE fl_verify_status = 'PENDING'")
        pending_freelancers = int(cursor.fetchone()["c"])
        cursor.execute("SELECT COUNT(*) AS c FROM jobs WHERE job_status = 'OPEN'")
        open_jobs = int(cursor.fetchone()["c"])
        cursor.execute("SELECT COUNT(*) AS c FROM jobs WHERE job_status = 'IN_PROGRESS'")
        in_progress_jobs = int(cursor.fetchone()["c"])
        cursor.execute("SELECT COUNT(*) AS c FROM jobs WHERE job_status = 'COMPLETED'")
        completed_jobs = int(cursor.fetchone()["c"])
        conn.close()
        return {
            "totalJobs": totalJobs,
            "openJobs": open_jobs,
            "inProgressJobs": in_progress_jobs,
            "completedJobs": completed_jobs,
            "employers": total_employers,
            "freelancers": total_freelancers,
            "pendingVerify": pending_employers + pending_freelancers,
            "pendingEmployers": pending_employers,
            "pendingFreelancers": pending_freelancers,
        }
    except Exception as e:
        return {"error": str(e)}


@router.get("/admins")
def admin_admins(limit: int = 50, offset: int = 0):
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute(
            "SELECT admin_id, name, status, created_at FROM admins ORDER BY created_at DESC LIMIT %s OFFSET %s",
            (limit, offset)
        )
        rows = cursor.fetchall()
        conn.close()
        return {"items": rows, "limit": limit, "offset": offset}
    except Exception as e:
        return {"error": str(e), "items": []}


@router.post("/login")
def admin_login(request: LoginRequest):
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute(
            "SELECT admin_id, username, email, name, password_hash, status, created_at, updated_at FROM admins WHERE username = %s",
            (request.username,)
        )
        row = cursor.fetchone()
        cursor.close()
        conn.close()

        if row:
            try:
                match = bcrypt.checkpw(request.password.encode('utf-8'), row["password_hash"].encode('utf-8'))
            except Exception as verify_err:
                return {"success": False, "error": f"Verify error: {str(verify_err)}"}

            if match:
                return {
                    "success": True,
                    "admin": {
                        "admin_id": row["admin_id"],
                        "username": row["username"],
                        "email": row["email"],
                        "name": row["name"],
                        "status": row["status"],
                        "created_at": row["created_at"],
                        "updated_at": row["updated_at"]
                    }
                }
            else:
                return {"success": False, "error": "Wrong password"}
        else:
            return {"success": False, "error": "Admin not found"}
    except Exception as e:
        return {"success": False, "error": f"DB error: {str(e)}"}


@router.get("/me")
def admin_me(admin_id: str):
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute(
            "SELECT admin_id, username, email, name, status, created_at, updated_at FROM admins WHERE admin_id = %s",
            (admin_id,)
        )
        row = cursor.fetchone()
        conn.close()
        if row:
            return row
        return {"error": "Admin not found"}
    except Exception as e:
        return {"error": str(e)}


@router.get("/logs")
def admin_logs(limit: int = 50, offset: int = 0,
               action_type: Optional[str] = None, target_type: Optional[str] = None):
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        where = []
        params = []
        if action_type:
            where.append("al.action_type = %s")
            params.append(action_type)
        if target_type:
            where.append("al.target_type = %s")
            params.append(target_type)
        where_clause = ("WHERE " + " AND ".join(where)) if where else ""
        cursor.execute(
            f"""
            SELECT al.log_id, a.name AS admin_name,
                   al.action_type, al.target_type,
                   al.target_id, al.target_name, al.note, al.created_at
            FROM admin_logs al
            JOIN admins a ON al.admin_id = a.admin_id
            {where_clause}
            ORDER BY al.created_at DESC
            LIMIT %s OFFSET %s
            """,
            (*params, limit, offset)
        )
        rows = cursor.fetchall()
        conn.close()
        return {"items": rows, "limit": limit, "offset": offset}
    except Exception as e:
        return {"error": str(e), "items": []}


@router.post("/log")
def create_admin_log(body: LogRequest):
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute(
            "INSERT INTO admin_logs (admin_id, action_type, target_type, target_id, target_name, note) VALUES (%s, %s, %s, %s, %s, %s)",
            (body.admin_id, body.action_type, body.target_type, body.target_id, body.target_name, body.note)
        )
        conn.commit()
        conn.close()
        return {"status": "logged"}
    except Exception as e:
        return {"error": str(e)}
