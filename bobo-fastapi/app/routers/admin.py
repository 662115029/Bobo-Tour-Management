from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from typing import Optional
from app.db.connection import get_connection, get_cursor
from .utils import (
    validate_password,
    normalize_admin_login_identifier,
    validate_profile_update_fields,
)
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


class AdminUpdateRequest(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    status: Optional[str] = None


class AdminRegisterRequest(BaseModel):
    username: str
    email: str
    name: str
    password: str


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str


@router.get("/db/ping")
def admin_db_ping():
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute("SELECT 1 AS ok")
        row = cursor.fetchone()
        return {"db": "mysql", "connected": True, "ok": row["ok"]}
    except Exception as e:
        return {"db": "mysql", "connected": False, "error": str(e)}
    finally:
        if conn:
            conn.close()


@router.get("/stats")
def admin_stats():
    conn = None
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
    finally:
        if conn:
            conn.close()


@router.get("/admins")
def admin_admins(limit: int = 50, offset: int = 0):
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute(
            """
            SELECT admin_id, username, email, name, status, created_at, updated_at
            FROM admins
            ORDER BY created_at DESC
            LIMIT %s OFFSET %s
            """,
            (limit, offset)
        )
        rows = cursor.fetchall()
        return {"items": rows, "limit": limit, "offset": offset}
    except Exception as e:
        return {"error": str(e), "items": []}
    finally:
        if conn:
            conn.close()


@router.post("/log")
def create_admin_log(body: LogRequest):
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute(
            """
            INSERT INTO admin_logs
                (admin_id, action_type, target_type, target_id, target_name, note)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (body.admin_id, body.action_type, body.target_type,
             body.target_id, body.target_name, body.note)
        )
        conn.commit()
        return {"status": "logged"}
    except Exception as e:
        return {"error": str(e)}
    finally:
        if conn:
            conn.close()


@router.post("/login")
def admin_login(request: LoginRequest):
    conn = None
    try:
        pwd_raw = request.password if request.password is not None else ""
        pwd_str = str(pwd_raw).strip()
        if not pwd_str:
            return {"success": False, "error": "Password is missing." + _RETRY}

        lookup_key, ident_err = normalize_admin_login_identifier(request.username)
        if ident_err:
            return {"success": False, "error": ident_err}

        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute(
            """
            SELECT admin_id, username, email, name, password_hash, status, created_at, updated_at
            FROM admins
            WHERE username = %s OR email = %s
            """,
            (lookup_key, lookup_key)
        )
        row = cursor.fetchone()

        if row:
            if (row.get("status") or "").lower() != "active":
                return {
                    "success": False,
                    "error": "This admin account is inactive and cannot sign in. Contact an administrator.",
                }
            ph = row["password_hash"]
            ph_bytes = ph if isinstance(ph, bytes) else str(ph).encode("utf-8")
            try:
                match = bcrypt.checkpw(pwd_str.encode("utf-8"), ph_bytes)
            except ValueError:
                return {
                    "success": False,
                    "error": "The stored password for this account is not configured correctly (invalid hash). An administrator must update password_hash in the database.",
                }
            except Exception as verify_err:
                return {
                    "success": False,
                    "error": f"Password could not be verified ({str(verify_err)}). Please try again or contact support.",
                }

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
                        "updated_at": row["updated_at"],
                    },
                }
            else:
                return {"success": False, "error": "The password is incorrect (check Caps Lock and spelling)." + _RETRY}
        else:
            return {"success": False, "error": "No admin account matches that username or email." + _RETRY}
    except Exception as e:
        return {"success": False, "error": f"Server or database error: {str(e)}. Please try again later."}
    finally:
        if conn:
            conn.close()


@router.get("/me")
def admin_me(x_admin_id: str = Header(None, alias="X-Admin-ID")):
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute(
            """
            SELECT admin_id, username, email, name, status, created_at, updated_at
            FROM admins WHERE admin_id = %s
            """,
            (x_admin_id,)
        )
        row = cursor.fetchone()
        if row:
            return {
                "admin_id": row["admin_id"],
                "username": row["username"],
                "email": row["email"],
                "name": row["name"],
                "status": row["status"],
                "created_at": row["created_at"],
                "updated_at": row["updated_at"],
            }
        return {"error": "Admin not found"}
    except Exception as e:
        return {"error": str(e)}
    finally:
        if conn:
            conn.close()


@router.patch("/{admin_id}")
def update_admin(admin_id: str, body: AdminUpdateRequest):
    conn = None
    try:
        fields = {}
        if body.name is not None:
            fields["name"] = body.name.strip()
        if body.email is not None:
            fields["email"] = body.email.strip()
        if body.status is not None and body.status in ("active", "inactive"):
            fields["status"] = body.status
        if not fields:
            return {"error": validate_profile_update_fields(fields)}

        set_clause = ", ".join(f"{k} = %s" for k in fields)
        values = list(fields.values()) + [admin_id]

        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute(
            f"UPDATE admins SET {set_clause}, updated_at = NOW() WHERE admin_id = %s",
            values
        )
        conn.commit()
        cursor.execute("SELECT updated_at FROM admins WHERE admin_id = %s", (admin_id,))
        row = cursor.fetchone()
        return {"status": "updated", "updated_at": row["updated_at"] if row else None}
    except Exception as e:
        return {"error": str(e)}
    finally:
        if conn:
            conn.close()

@router.post("/{admin_id}/change-password")
def change_admin_password(admin_id: str, body: ChangePasswordRequest):
    conn = None
    try:
        current_password = body.current_password
        new_password = body.new_password

        if not current_password or not new_password:
            return {"success": False, "error": "Both current and new passwords are required."}
        pwd_err = validate_password(new_password, min_length=8)
        if pwd_err:
            return {"success": False, "error": f"New password: {pwd_err}"}

        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute("SELECT password_hash FROM admins WHERE admin_id = %s", (admin_id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Admin not found.")

        if not bcrypt.checkpw(current_password.encode(), row["password_hash"].encode()):
            return {"success": False, "error": "Current password is incorrect."}

        new_hash = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
        cursor.execute(
            "UPDATE admins SET password_hash = %s, updated_at = NOW() WHERE admin_id = %s",
            (new_hash, admin_id)
        )
        conn.commit()
        return {"success": True, "message": "Password changed successfully."}
    except Exception as e:
        return {"success": False, "error": str(e)}
    finally:
        if conn:
            conn.close()


@router.get("/logs")
def admin_logs(limit: int = 50, offset: int = 0,
               action_type: str = None, target_type: str = None,
               year: int = None, month: str = None, search: str = None):
    conn = None
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
        if year:
            where.append("YEAR(al.created_at) = %s")
            params.append(year)
        if month:
            where.append("MONTH(al.created_at) = %s")
            params.append(int(month))
        if search:
            where.append("(al.target_name LIKE %s OR al.action_type LIKE %s OR al.note LIKE %s)")
            params += [f"%{search}%", f"%{search}%", f"%{search}%"]
        where_clause = ("WHERE " + " AND ".join(where)) if where else ""
        cursor.execute(
            f"""
            SELECT al.log_id, a.name AS admin_name,
                   al.action_type, al.target_type,
                   al.target_id, al.target_name, al.note,
                   al.created_at
            FROM admin_logs al
            LEFT JOIN admins a ON al.admin_id = a.admin_id
            {where_clause}
            ORDER BY al.created_at DESC
            LIMIT %s OFFSET %s
            """,
            (*params, limit, offset)
        )
        rows = cursor.fetchall()
        return {"items": rows, "limit": limit, "offset": offset}
    except Exception as e:
        return {"error": str(e), "items": []}
    finally:
        if conn:
            conn.close()


@router.get("/matching-config")
def get_matching_config():
    """Returns the current matching formula weights."""
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute(
            """
            SELECT weight_pickup_area, weight_availability,
                   weight_verification, weight_language, updated_at
            FROM matching_config
            WHERE id = 1
            """
        )
        config = cursor.fetchone()
        if not config:
            raise HTTPException(status_code=404, detail="Matching config not found.")
        return config
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()


@router.put("/matching-config")
def update_matching_config(data: dict):
    """
    Updates the matching formula weights. All four weights are required and
    must sum to exactly 100 — enforced here AND at the database level
    (matching_config has a CHECK constraint), so this can never be violated
    even if another endpoint writes to this table in the future.
    """
    required_fields = [
        "weight_pickup_area", "weight_availability",
        "weight_verification", "weight_language",
    ]
    missing = [f for f in required_fields if f not in data]
    if missing:
        raise HTTPException(
            status_code=400,
            detail=f"Missing required field(s): {', '.join(missing)}",
        )

    weights = {}
    for field in required_fields:
        value = data[field]
        if not isinstance(value, int) or isinstance(value, bool):
            raise HTTPException(status_code=400, detail=f"{field} must be an integer.")
        if value < 0 or value > 100:
            raise HTTPException(status_code=400, detail=f"{field} must be between 0 and 100.")
        weights[field] = value

    total = sum(weights.values())
    if total != 100:
        raise HTTPException(
            status_code=400,
            detail=f"Weights must sum to exactly 100 (got {total}). "
                   f"Received: {weights}",
        )

    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute(
            """
            UPDATE matching_config
            SET weight_pickup_area = %s,
                weight_availability = %s,
                weight_verification = %s,
                weight_language = %s
            WHERE id = 1
            """,
            (
                weights["weight_pickup_area"],
                weights["weight_availability"],
                weights["weight_verification"],
                weights["weight_language"],
            ),
        )
        conn.commit()
        return {"success": True, "weights": weights}
    except HTTPException:
        raise
    except Exception as e:
        if conn:
            conn.rollback()
        # if the DB-level CHECK constraint somehow catches something the
        # application check above missed, it surfaces here as a normal error
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()