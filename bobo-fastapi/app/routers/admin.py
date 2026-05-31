from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from typing import Optional, Tuple
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


_RETRY = " Please verify your details and try again."


def _normalize_admin_login_identifier(raw: str) -> Tuple[Optional[str], Optional[str]]:
    """Strip input; if it looks like an email, require domain admin.com."""
    s = (raw or "").strip()
    if not s:
        return (None, "Username or email is missing." + _RETRY)
    if "@" in s:
        local, _, domain = s.rpartition("@")
        domain_clean = domain.strip()
        if not local or not domain_clean or "@" in local:
            return (None, "That email address is not valid (check the part before and after @)." + _RETRY)
        dom_lower = domain_clean.lower()
        if dom_lower != "admin.com":
            return (None, f"Admin email must use the domain @admin.com only (you entered: {domain_clean})." + _RETRY)
        return s.lower(), None
    return s, None


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

        lookup_key, ident_err = _normalize_admin_login_identifier(request.username)
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
            return {"error": "No fields to update"}

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


@router.post("/register")
def admin_register(body: AdminRegisterRequest):
    conn = None
    try:
        username = body.username.strip()
        email = body.email.strip()
        name = body.name.strip()
        password = body.password

        if not username or not email or not name or not password:
            return {"success": False, "error": "All fields are required."}
        if not email.lower().endswith("@admin.com"):
            return {"success": False, "error": "Email must use the @admin.com domain."}
        if len(password) < 6:
            return {"success": False, "error": "Password must be at least 6 characters."}

        conn = get_connection()
        cursor = get_cursor(conn)

        cursor.execute("SELECT admin_id FROM admins WHERE username = %s", (username,))
        if cursor.fetchone():
            return {"success": False, "error": "Username already taken."}

        cursor.execute("SELECT admin_id FROM admins WHERE email = %s", (email,))
        if cursor.fetchone():
            return {"success": False, "error": "Email already registered."}

        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        cursor.execute(
            """
            INSERT INTO admins (admin_id, username, email, name, password_hash, status)
            VALUES (UUID(), %s, %s, %s, %s, 'active')
            """,
            (username, email, name, password_hash)
        )
        conn.commit()
        cursor.execute(
            "SELECT admin_id, username, email, name, status, created_at FROM admins WHERE username = %s",
            (username,)
        )
        row = cursor.fetchone()
        return {
            "success": True,
            "admin": {
                "admin_id": row["admin_id"],
                "username": row["username"],
                "email": row["email"],
                "name": row["name"],
                "status": row["status"],
                "created_at": row["created_at"],
            },
        }
    except Exception as e:
        return {"success": False, "error": str(e)}
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
        if len(new_password) < 6:
            return {"success": False, "error": "New password must be at least 6 characters."}

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