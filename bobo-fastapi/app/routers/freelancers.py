from fastapi import APIRouter, HTTPException, Body
import bcrypt
from pydantic import BaseModel
from typing import Optional
from app.db.connection import get_connection, get_cursor

router = APIRouter(tags=["freelancers"])

FL_DOC_TYPES = [
    "PERSONAL_ID",
    "DRIVER_LICENSE",
    "PUBLIC_DRIVER_LICENSE",
    "VEHICLE_REGISTRATION",
    "VEHICLE_INSPECTION",
]


class FreelancerRegisterRequest(BaseModel):
    fl_username: str
    fl_email: str
    fl_name: str
    fl_phone: str
    fl_password: str
    line_user_id: Optional[str] = None


class DocReviewRequest(BaseModel):
    status: str
    reviewed_by: str
    note: Optional[str] = None
    reason: Optional[str] = None


class BanRequest(BaseModel):
    is_active: bool
    admin_id: str


@router.post("/freelancers/register")
def register_freelancer(body: FreelancerRegisterRequest):
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)

        cursor.execute(
            "SELECT fl_id FROM freelancers WHERE fl_email = %s OR fl_username = %s",
            (body.fl_email, body.fl_username)
        )
        if cursor.fetchone():
            raise HTTPException(status_code=409, detail="Email or username already taken.")

        cursor.execute(
            """
            INSERT INTO freelancers
                (line_user_id, fl_username, fl_email, fl_name, fl_phone,
                 fl_verify_status, fl_is_active)
            VALUES (%s, %s, %s, %s, %s, 'PENDING', 1)
            """,
            (body.line_user_id, body.fl_username,
             body.fl_email, body.fl_name, body.fl_phone)
        )
        fl_id = cursor.lastrowid

        cursor.execute(
            """
            INSERT INTO fl_verification
                (fl_id, fl_verify_status, is_latest)
            VALUES (%s, 'PENDING', 1)
            """,
            (fl_id,)
        )

        for doc_type in FL_DOC_TYPES:
            cursor.execute(
                """
                INSERT INTO fl_documents
                    (fl_id, fl_doc_type, file_url, fl_doc_status)
                VALUES (%s, %s, NULL, 'PENDING')
                """,
                (fl_id, doc_type)
            )

        conn.commit()
        return {"success": True, "fl_id": fl_id}

    except HTTPException:
        raise
    except Exception as e:
        if conn:
            conn.rollback()
        return {"success": False, "error": str(e)}
    finally:
        if conn:
            conn.close()
@router.get("/freelancers")
@router.get("/admin/freelancers")
def get_freelancers(limit: int = 10, offset: int = 0, search: str = "", status: str = "", sort_by: str = "fl_updated_at", sort_order: str = "desc"):
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        where = []
        params = []
        if search:
            where.append("(fl_name LIKE %s OR fl_username LIKE %s)")
            params += [f"%{search}%", f"%{search}%"]
        if status:
            where.append("fl_verify_status = %s")
            params.append(status)
        where_sql = "WHERE " + " AND ".join(where) if where else ""
        params += [limit, offset]
        allowed_sort = {"fl_name","fl_rating_avg","fl_updated_at","fl_created_at"}
        safe_sort_by = sort_by if sort_by in allowed_sort else "fl_updated_at"
        safe_order = "ASC" if sort_order.lower() == "asc" else "DESC"
        cursor.execute(
            f"""
            SELECT fl_id, line_user_id, fl_username, fl_email, fl_name, fl_date_of_birth,
                   fl_phone, fl_address, fl_bio, fl_profile_image_url,
                   fl_verify_status, fl_is_active, fl_rating_avg,
                   fl_created_at, fl_updated_at
            FROM freelancers
            {where_sql}
            ORDER BY {safe_sort_by} {safe_order}
            LIMIT %s OFFSET %s
            """,
            params
        )
        rows = cursor.fetchall()
        return {"items": rows, "limit": limit, "offset": offset, "search": search, "status": status}
    except Exception as e:
        return {"error": str(e), "items": []}
    finally:
        if conn:
            conn.close()
@router.get("/freelancers/{fl_id}")
def get_freelancer(fl_id: str):
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute(
            """
            SELECT fl_id, line_user_id, fl_username, fl_email, fl_name, fl_date_of_birth,
                   fl_phone, fl_address, fl_bio, fl_profile_image_url,
                   fl_verify_status, fl_is_active, fl_rating_avg,
                   fl_created_at, fl_updated_at
            FROM freelancers
            WHERE fl_id = %s
            """,
            (fl_id,)
        )
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Freelancer not found")
        return row
    except HTTPException:
        raise
    except Exception as e:
        return {"error": str(e)}
    finally:
        if conn:
            conn.close()
@router.get("/fl-bank-accounts")
def get_fl_bank_accounts(limit: int = 10, offset: int = 0, fl_id: Optional[int] = None):
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        where_sql = "WHERE fb.fl_id = %s" if fl_id else ""
        params = ([fl_id] if fl_id else []) + [limit, offset]
        cursor.execute(
            f"""
            SELECT fb.fl_bank_account_id, fb.fl_id, f.fl_name,
                   fb.account_name, fb.account_number, fb.bank_name,
                   fb.is_primary, fb.created_at, fb.updated_at
            FROM fl_bank_accounts fb
            JOIN freelancers f ON fb.fl_id = f.fl_id
            {where_sql}
            ORDER BY fb.created_at DESC
            LIMIT %s OFFSET %s
            """,
            params
        )
        rows = cursor.fetchall()
        return {"items": rows, "limit": limit, "offset": offset}
    except Exception as e:
        return {"error": str(e), "items": []}
    finally:
        if conn:
            conn.close()
@router.get("/fl-vehicle")
def get_fl_vehicle(limit: int = 10, offset: int = 0, fl_id: Optional[int] = None):
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        where_sql = "WHERE fv.fl_id = %s" if fl_id else ""
        params = ([fl_id] if fl_id else []) + [limit, offset]
        cursor.execute(
            f"""
            SELECT fv.fl_vehicle_id, fv.fl_id, f.fl_name,
                   fv.fl_vehicle_type, fv.fl_vehicle_brand, fv.fl_vehicle_model,
                   fv.fl_vehicle_year, fv.fl_vehicle_seat_capa,
                   fv.fl_vehicle_license_plate,
                   fv.fl_vehicle_created_at, fv.fl_vehicle_updated_at
            FROM fl_vehicle fv
            JOIN freelancers f ON fv.fl_id = f.fl_id
            {where_sql}
            ORDER BY fv.fl_vehicle_created_at DESC
            LIMIT %s OFFSET %s
            """,
            params
        )
        rows = cursor.fetchall()
        return {"items": rows, "limit": limit, "offset": offset}
    except Exception as e:
        return {"error": str(e), "items": []}
    finally:
        if conn:
            conn.close()
@router.get("/fl-vehicle-images")
def get_fl_vehicle_images(limit: int = 10, offset: int = 0, fl_id: Optional[int] = None):
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        where_sql = "WHERE fv.fl_id = %s" if fl_id else ""
        params = ([fl_id] if fl_id else []) + [limit, offset]
        cursor.execute(
            f"""
            SELECT fvi.fl_vehicle_image_id, fvi.fl_vehicle_id,
                   fv.fl_vehicle_brand, fv.fl_vehicle_model,
                   fv.fl_vehicle_license_plate, f.fl_name,
                   fvi.fl_vehicle_image_url, fvi.uploaded_at
            FROM fl_vehicle_images fvi
            JOIN fl_vehicle fv ON fvi.fl_vehicle_id = fv.fl_vehicle_id
            JOIN freelancers f ON fv.fl_id = f.fl_id
            {where_sql}
            ORDER BY fvi.uploaded_at DESC
            LIMIT %s OFFSET %s
            """,
            params
        )
        rows = cursor.fetchall()
        return {"items": rows, "limit": limit, "offset": offset}
    except Exception as e:
        return {"error": str(e), "items": []}
    finally:
        if conn:
            conn.close()
@router.get("/fl-languages")
def get_fl_languages(limit: int = 10, offset: int = 0, fl_id: Optional[int] = None):
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        where_sql = "WHERE fl.fl_id = %s" if fl_id else ""
        params = ([fl_id] if fl_id else []) + [limit, offset]
        cursor.execute(
            f"""
            SELECT fl.fl_id, f.fl_name,
                   l.language_id, l.language_name
            FROM fl_languages fl
            JOIN freelancers f ON fl.fl_id = f.fl_id
            JOIN languages l ON fl.language_id = l.language_id
            {where_sql}
            ORDER BY f.fl_name, l.language_name
            LIMIT %s OFFSET %s
            """,
            params
        )
        rows = cursor.fetchall()
        return {"items": rows, "limit": limit, "offset": offset}
    except Exception as e:
        return {"error": str(e), "items": []}
    finally:
        if conn:
            conn.close()
@router.get("/fl-pickup-areas")
def get_fl_pickup_areas(limit: int = 10, offset: int = 0, fl_id: Optional[int] = None):
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        where_sql = "WHERE fp.fl_id = %s" if fl_id else ""
        params = ([fl_id] if fl_id else []) + [limit, offset]
        cursor.execute(
            f"""
            SELECT fp.fl_id, f.fl_name,
                   a.area_id, a.area_name
            FROM fl_pickup_areas fp
            JOIN freelancers f ON fp.fl_id = f.fl_id
            JOIN areas a ON fp.area_id = a.area_id
            {where_sql}
            ORDER BY f.fl_name, a.area_name
            LIMIT %s OFFSET %s
            """,
            params
        )
        rows = cursor.fetchall()
        return {"items": rows, "limit": limit, "offset": offset}
    except Exception as e:
        return {"error": str(e), "items": []}
    finally:
        if conn:
            conn.close()
@router.get("/fl-availability")
def get_fl_availability(limit: int = 10, offset: int = 0, fl_id: Optional[int] = None):
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        where_sql = "WHERE fa.fl_id = %s" if fl_id else ""
        params = ([fl_id] if fl_id else []) + [limit, offset]
        cursor.execute(
            f"""
            SELECT fa.fl_available_id, fa.fl_id, f.fl_name,
                   fa.fl_available_start_date, fa.fl_available_end_date,
                   fa.is_active, fa.created_at, fa.updated_at
            FROM fl_availability fa
            JOIN freelancers f ON fa.fl_id = f.fl_id
            {where_sql}
            ORDER BY fa.fl_available_start_date DESC
            LIMIT %s OFFSET %s
            """,
            params
        )
        rows = cursor.fetchall()
        return {"items": rows, "limit": limit, "offset": offset}
    except Exception as e:
        return {"error": str(e), "items": []}
    finally:
        if conn:
            conn.close()
@router.get("/fl-documents")
def get_fl_documents(limit: int = 10, offset: int = 0, status: str = "", fl_id: Optional[int] = None, fl_ids: str = ""):
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        where = []
        params = []
        if fl_id:
            where.append("fd.fl_id = %s")
            params.append(fl_id)
        elif fl_ids:
            id_list = [int(i) for i in fl_ids.split(',') if i.strip().isdigit()]
            placeholders = ','.join(['%s'] * len(id_list))
            where.append(f"fd.fl_id IN ({placeholders})")
            params += id_list
        if status:
            where.append("fd.fl_doc_status = %s")
            params.append(status)
        elif not fl_id and not fl_ids:
            where.append("fd.file_url IS NOT NULL")
        where_sql = "WHERE " + " AND ".join(where) if where else ""
        params += [limit, offset]
        cursor.execute(
            f"""
            SELECT fd.fl_doc_id, fd.fl_id, f.fl_name,
                   fd.fl_doc_type, fd.file_url, fd.fl_doc_status,
                   fd.fl_uploaded_at, fd.reject_reason,
                   a.name AS reviewed_by_name, fd.reviewed_at
            FROM fl_documents fd
            JOIN freelancers f ON fd.fl_id = f.fl_id
            LEFT JOIN admins a ON fd.reviewed_by = a.admin_id
            {where_sql}
            ORDER BY fd.fl_uploaded_at ASC
            LIMIT %s OFFSET %s
            """,
            params
        )
        rows = cursor.fetchall()
        return {"items": rows, "limit": limit, "offset": offset}
    except Exception as e:
        return {"error": str(e), "items": []}
    finally:
        if conn:
            conn.close()
@router.get("/fl-verification")
def get_fl_verification(limit: int = 10, offset: int = 0, status: str = "PENDING", fl_id: Optional[int] = None):
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        where = []
        params = []
        if fl_id:
            where.append("fv.fl_id = %s")
            params.append(fl_id)
        if status:
            where.append("fv.fl_verify_status = %s")
            params.append(status)
        where_sql = ("WHERE " + " AND ".join(where)) if where else ""
        params += [limit, offset]
        cursor.execute(
            f"""
            SELECT fv.fl_verify_id, fv.fl_id, f.fl_name,
                   fv.fl_verify_status, fv.is_latest,
                   fv.fl_submitted_at, fv.fl_verified_at,
                   a.name AS reviewed_by_name
            FROM fl_verification fv
            JOIN freelancers f ON fv.fl_id = f.fl_id
            LEFT JOIN admins a ON fv.reviewed_by = a.admin_id
            {where_sql}
            ORDER BY fv.fl_submitted_at ASC
            LIMIT %s OFFSET %s
            """,
            params
        )
        rows = cursor.fetchall()
        return {"items": rows, "limit": limit, "offset": offset}
    except Exception as e:
        return {"error": str(e), "items": []}
    finally:
        if conn:
            conn.close()
@router.patch("/fl-documents/{doc_id}")
def review_fl_document(doc_id: str, body: DocReviewRequest):
    if body.status not in ("APPROVED", "REJECTED", "PENDING"):
        raise HTTPException(status_code=400, detail="status must be APPROVED, REJECTED, or PENDING")
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute("SELECT fl_doc_id, fl_id FROM fl_documents WHERE fl_doc_id = %s", (doc_id,))
        doc = cursor.fetchone()
        if not doc:
            raise HTTPException(status_code=404, detail="Document not found")

        reject_reason = body.reason if body.status == "REJECTED" else None
        cursor.execute(
            """
            UPDATE fl_documents
            SET fl_doc_status = %s, reviewed_by = %s, reviewed_at = NOW(),
                reject_reason = %s
            WHERE fl_doc_id = %s
            """,
            (body.status, body.reviewed_by, reject_reason, doc_id)
        )

        if body.status == "APPROVED":
            cursor.execute(
                """
                SELECT COUNT(*) AS c FROM fl_documents
                WHERE fl_id = %s AND fl_doc_status != 'APPROVED' AND file_url IS NOT NULL
                """,
                (doc["fl_id"],)
            )
            if cursor.fetchone()["c"] == 0:
                cursor.execute(
                    "UPDATE freelancers SET fl_verify_status = 'VERIFIED' WHERE fl_id = %s",
                    (doc["fl_id"],)
                )
                cursor.execute(
                    """
                    UPDATE fl_verification SET fl_verify_status = 'VERIFIED',
                    fl_verified_at = NOW(), reviewed_by = %s
                    WHERE fl_id = %s AND is_latest = 1
                    """,
                    (body.reviewed_by, doc["fl_id"])
                )
            else:
                cursor.execute(
                    "UPDATE freelancers SET fl_verify_status = 'PENDING' WHERE fl_id = %s",
                    (doc["fl_id"],)
                )
        elif body.status == "REJECTED":
            cursor.execute(
                """
                SELECT
                  SUM(CASE WHEN fl_doc_status = 'REJECTED' THEN 1 ELSE 0 END) AS rejected,
                  SUM(CASE WHEN fl_doc_status = 'PENDING' THEN 1 ELSE 0 END) AS pending,
                  SUM(CASE WHEN fl_doc_status = 'APPROVED' THEN 1 ELSE 0 END) AS approved,
                  COUNT(*) AS total
                FROM fl_documents
                WHERE fl_id = %s AND file_url IS NOT NULL
                """,
                (doc["fl_id"],)
            )
            counts = cursor.fetchone()
            all_rejected = counts["total"] > 0 and counts["pending"] == 0 and counts["approved"] == 0
            if all_rejected:
                cursor.execute(
                    "UPDATE freelancers SET fl_verify_status = 'NOT_VERIFIED' WHERE fl_id = %s",
                    (doc["fl_id"],)
                )
                cursor.execute(
                    """
                    UPDATE fl_verification SET fl_verify_status = 'NOT_VERIFIED'
                    WHERE fl_id = %s AND is_latest = 1
                    """,
                    (doc["fl_id"],)
                )

            else:
                cursor.execute(
                    "UPDATE freelancers SET fl_verify_status = 'PENDING' WHERE fl_id = %s",
                    (doc["fl_id"],)
                )
                cursor.execute(
                    """
                    UPDATE fl_verification SET fl_verify_status = 'PENDING'
                    WHERE fl_id = %s AND is_latest = 1
                    """,
                    (doc["fl_id"],)
                )

        if body.status == "PENDING":
            cursor.execute(
                "UPDATE freelancers SET fl_verify_status = 'PENDING' WHERE fl_id = %s",
                (doc["fl_id"],)
            )
            cursor.execute(
                """
                UPDATE fl_verification SET fl_verify_status = 'PENDING'
                WHERE fl_id = %s AND is_latest = 1
                """,
                (doc["fl_id"],)
            )

        cursor.execute(
            """
            SELECT f.fl_name, fd.fl_doc_type
            FROM fl_documents fd
            JOIN freelancers f ON fd.fl_id = f.fl_id
            WHERE fd.fl_doc_id = %s
            """,
            (doc_id,)
        )
        doc_info = cursor.fetchone()
        if doc_info:
            doc_label = doc_info["fl_doc_type"].replace('_', ' ').title()
            if body.status == 'REJECTED':
                log_note = f"{doc_label}: {body.reason}" if body.reason else doc_label
                cursor.execute(
                    """
                    INSERT INTO admin_logs
                        (admin_id, action_type, target_type, target_id, target_name, note)
                    VALUES (%s, 'REJECT_DOCUMENT', 'DOCUMENT', %s, %s, %s)
                    """,
                    (body.reviewed_by, doc_id, doc_info["fl_name"], log_note)
                )
                if all_rejected:
                    cursor.execute("SELECT fl_name FROM freelancers WHERE fl_id = %s", (doc["fl_id"],))
                    fl_info = cursor.fetchone()
                    cursor.execute(
                        """
                        INSERT INTO admin_logs
                            (admin_id, action_type, target_type, target_id, target_name, note)
                        VALUES (%s, 'NOT_VERIFY_FREELANCER', 'FREELANCER', %s, %s, 'All uploaded documents rejected')
                        """,
                        (body.reviewed_by, doc["fl_id"], fl_info["fl_name"] if fl_info else doc["fl_id"])
                    )
            elif body.status == "APPROVED":
                cursor.execute(
                    """
                    INSERT INTO admin_logs
                        (admin_id, action_type, target_type, target_id, target_name, note)
                    VALUES (%s, 'APPROVE_DOCUMENT', 'DOCUMENT', %s, %s, %s)
                    """,
                    (body.reviewed_by, doc_id, doc_info["fl_name"], doc_label)
                )
                cursor.execute(
                    """
                    SELECT COUNT(*) AS c FROM fl_documents 
                    WHERE fl_id = %s AND fl_doc_status != 'APPROVED' AND file_url IS NOT NULL
                    """,
                    (doc["fl_id"],)
                )
                if cursor.fetchone()["c"] == 0:
                    cursor.execute("SELECT fl_name FROM freelancers WHERE fl_id = %s", (doc["fl_id"],))
                    fl_info = cursor.fetchone()
                    cursor.execute(
                        """
                        INSERT INTO admin_logs
                            (admin_id, action_type, target_type, target_id, target_name, note)
                        VALUES (%s, 'VERIFY_FREELANCER', 'FREELANCER', %s, %s, 'All documents approved')
                        """,
                        (body.reviewed_by, doc["fl_id"], fl_info["fl_name"] if fl_info else doc["fl_id"])
                    )

        conn.commit()
        return {"status": "updated", "doc_id": doc_id, "new_status": body.status}
    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR] review_fl_document: {e}")
        if conn:
            conn.rollback()
        return {"error": str(e)}
    finally:
        if conn:
            conn.close()
@router.patch("/freelancers/{fl_id}/ban")
def ban_freelancer(fl_id: str, body: BanRequest):
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute("SELECT fl_id FROM freelancers WHERE fl_id = %s", (fl_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Freelancer not found")
        cursor.execute(
            "UPDATE freelancers SET fl_is_active = %s WHERE fl_id = %s",
            (body.is_active, fl_id)
        )
        cursor.execute("SELECT fl_name FROM freelancers WHERE fl_id = %s", (fl_id,))
        fl_info = cursor.fetchone()
        action = 'UNBAN_USER' if body.is_active else 'BAN_USER'
        cursor.execute(
            """
            INSERT INTO admin_logs
                (admin_id, action_type, target_type, target_id, target_name, note)
            VALUES (%s, %s, 'FREELANCER', %s, %s, NULL)
            """,
            (body.admin_id, action, fl_id, fl_info["fl_name"] if fl_info else fl_id)
        )
        conn.commit()
        return {"status": "updated", "fl_id": fl_id, "is_active": body.is_active}
    except HTTPException:
        raise
    except Exception as e:
        return {"error": str(e)}
    finally:
        if conn:
            conn.close()

@router.get("/languages")
def get_languages():
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute("SELECT language_id, language_name FROM languages ORDER BY language_name ASC")
        return cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()


@router.post("/languages")
def create_or_get_language(data: dict):
    conn = None
    try:
        name = (data.get("language_name") or "").strip()
        if not name:
            raise HTTPException(status_code=400, detail="language_name is required")
        conn = get_connection()
        cursor = get_cursor(conn)
        # check if exists (case-insensitive)
        cursor.execute(
            "SELECT language_id, language_name FROM languages WHERE LOWER(language_name) = LOWER(%s)",
            (name,)
        )
        existing = cursor.fetchone()
        if existing:
            return existing
        # insert new
        cursor.execute("INSERT INTO languages (language_name) VALUES (%s)", (name,))
        conn.commit()
        return {"language_id": cursor.lastrowid, "language_name": name}
    except HTTPException:
        raise
    except Exception as e:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()

class FreelancerProfileUpdateRequest(BaseModel):
    fl_name: Optional[str] = None
    fl_email: Optional[str] = None
    fl_phone: Optional[str] = None
    fl_address: Optional[str] = None
    fl_bio: Optional[str] = None
    fl_date_of_birth: Optional[str] = None
    fl_profile_image_url: Optional[str] = None


@router.put("/freelancers/{fl_id}")
def update_freelancer(fl_id: str, body: FreelancerProfileUpdateRequest):
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute("SELECT fl_id FROM freelancers WHERE fl_id = %s", (fl_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Freelancer not found")
        cursor.execute(
            """
            UPDATE freelancers
            SET fl_name = COALESCE(%s, fl_name),
                fl_email = COALESCE(%s, fl_email),
                fl_phone = COALESCE(%s, fl_phone),
                fl_address = COALESCE(%s, fl_address),
                fl_bio = COALESCE(%s, fl_bio),
                fl_date_of_birth = COALESCE(%s, fl_date_of_birth),
                fl_profile_image_url = COALESCE(%s, fl_profile_image_url)
            WHERE fl_id = %s
            """,
            (body.fl_name, body.fl_email, body.fl_phone, body.fl_address,
             body.fl_bio, body.fl_date_of_birth, body.fl_profile_image_url, fl_id)
        )
        conn.commit()
        return {"success": True}
    except HTTPException:
        raise
    except Exception as e:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()


@router.patch("/freelancers/{fl_id}/pin")
def change_freelancer_pin(fl_id: str, data: dict):
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute("SELECT fl_pin_hash FROM freelancers WHERE fl_id = %s", (fl_id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Freelancer not found")
        current_pin = data.get("current_pin", "")
        if not bcrypt.checkpw(current_pin.encode(), row["fl_pin_hash"].encode()):
            raise HTTPException(status_code=401, detail="Incorrect current PIN.")
        new_pin = data.get("new_pin", "")
        if not new_pin or len(new_pin) != 6 or not new_pin.isdigit():
            raise HTTPException(status_code=400, detail="New PIN must be 6 digits.")
        new_hash = bcrypt.hashpw(new_pin.encode(), bcrypt.gensalt()).decode()
        cursor.execute("UPDATE freelancers SET fl_pin_hash = %s WHERE fl_id = %s", (new_hash, fl_id))
        conn.commit()
        return {"success": True}
    except HTTPException:
        raise
    except Exception as e:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()


class VehicleUpdateRequest(BaseModel):
    fl_vehicle_brand: Optional[str] = None
    fl_vehicle_model: Optional[str] = None
    fl_vehicle_year: Optional[int] = None
    fl_vehicle_seat_capa: Optional[int] = None
    fl_vehicle_license_plate: Optional[str] = None


@router.put("/fl-vehicle/{vehicle_id}")
def update_fl_vehicle(vehicle_id: str, body: VehicleUpdateRequest):
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute("SELECT fl_vehicle_id FROM fl_vehicle WHERE fl_vehicle_id = %s", (vehicle_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Vehicle not found")
        if body.fl_vehicle_seat_capa and not (9 <= body.fl_vehicle_seat_capa <= 13):
            raise HTTPException(status_code=400, detail="Seat capacity must be between 9 and 13.")
        cursor.execute(
            """
            UPDATE fl_vehicle
            SET fl_vehicle_brand         = COALESCE(%s, fl_vehicle_brand),
                fl_vehicle_model         = COALESCE(%s, fl_vehicle_model),
                fl_vehicle_year          = COALESCE(%s, fl_vehicle_year),
                fl_vehicle_seat_capa     = COALESCE(%s, fl_vehicle_seat_capa),
                fl_vehicle_license_plate = COALESCE(%s, fl_vehicle_license_plate)
            WHERE fl_vehicle_id = %s
            """,
            (body.fl_vehicle_brand, body.fl_vehicle_model, body.fl_vehicle_year,
             body.fl_vehicle_seat_capa, body.fl_vehicle_license_plate, vehicle_id)
        )
        conn.commit()
        return {"success": True}
    except HTTPException:
        raise
    except Exception as e:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()


@router.post("/fl-languages")
def add_fl_language(data: dict):
    conn = None
    try:
        fl_id = data.get("fl_id")
        language_name = (data.get("language_name") or "").strip()
        if not fl_id or not language_name:
            raise HTTPException(status_code=400, detail="fl_id and language_name are required.")
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute("SELECT language_id, language_name FROM languages WHERE LOWER(language_name) = LOWER(%s)", (language_name,))
        lang = cursor.fetchone()
        if not lang:
            cursor.execute("INSERT INTO languages (language_name) VALUES (%s)", (language_name,))
            language_id = cursor.lastrowid
            language_name_out = language_name
        else:
            language_id = lang["language_id"]
            language_name_out = lang["language_name"]
        cursor.execute("SELECT 1 FROM fl_languages WHERE fl_id = %s AND language_id = %s", (fl_id, language_id))
        if cursor.fetchone():
            raise HTTPException(status_code=409, detail="Language already added.")
        cursor.execute("INSERT INTO fl_languages (fl_id, language_id) VALUES (%s, %s)", (fl_id, language_id))
        conn.commit()
        return {"fl_id": fl_id, "language_id": language_id, "language_name": language_name_out}
    except HTTPException:
        raise
    except Exception as e:
        if conn: conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn: conn.close()


@router.delete("/fl-languages/{fl_id}/{language_id}")
def remove_fl_language(fl_id: int, language_id: int):
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute("DELETE FROM fl_languages WHERE fl_id = %s AND language_id = %s", (fl_id, language_id))
        conn.commit()
        return {"success": True}
    except Exception as e:
        if conn: conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn: conn.close()


@router.post("/fl-pickup-areas")
def add_fl_pickup_area(data: dict):
    conn = None
    try:
        fl_id = data.get("fl_id")
        area_name = (data.get("area_name") or "").strip()
        if not fl_id or not area_name:
            raise HTTPException(status_code=400, detail="fl_id and area_name are required.")
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute("SELECT area_id, area_name FROM areas WHERE LOWER(area_name) = LOWER(%s)", (area_name,))
        area = cursor.fetchone()
        if not area:
            cursor.execute("INSERT INTO areas (area_name) VALUES (%s)", (area_name,))
            area_id = cursor.lastrowid
            area_name_out = area_name
        else:
            area_id = area["area_id"]
            area_name_out = area["area_name"]
        cursor.execute("SELECT 1 FROM fl_pickup_areas WHERE fl_id = %s AND area_id = %s", (fl_id, area_id))
        if cursor.fetchone():
            raise HTTPException(status_code=409, detail="Area already added.")
        cursor.execute("INSERT INTO fl_pickup_areas (fl_id, area_id) VALUES (%s, %s)", (fl_id, area_id))
        conn.commit()
        return {"fl_id": fl_id, "area_id": area_id, "area_name": area_name_out}
    except HTTPException:
        raise
    except Exception as e:
        if conn: conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn: conn.close()


@router.delete("/fl-pickup-areas/{fl_id}/{area_id}")
def remove_fl_pickup_area(fl_id: int, area_id: int):
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute("DELETE FROM fl_pickup_areas WHERE fl_id = %s AND area_id = %s", (fl_id, area_id))
        conn.commit()
        return {"success": True}
    except Exception as e:
        if conn: conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn: conn.close()


class VehicleCreateRequest(BaseModel):
    fl_vehicle_brand: str
    fl_vehicle_model: str
    fl_vehicle_year: int
    fl_vehicle_seat_capa: int
    fl_vehicle_license_plate: str


@router.post("/fl-vehicle")
def create_fl_vehicle(body: VehicleCreateRequest, fl_id: int):
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        # check already has vehicle
        cursor.execute("SELECT fl_vehicle_id FROM fl_vehicle WHERE fl_id = %s", (fl_id,))
        if cursor.fetchone():
            raise HTTPException(status_code=409, detail="Vehicle already exists. Use PUT to update.")
        if not (9 <= body.fl_vehicle_seat_capa <= 13):
            raise HTTPException(status_code=400, detail="Seat capacity must be between 9 and 13.")
        cursor.execute(
            """
            INSERT INTO fl_vehicle
                (fl_id, fl_vehicle_type, fl_vehicle_brand, fl_vehicle_model,
                 fl_vehicle_year, fl_vehicle_seat_capa, fl_vehicle_license_plate)
            VALUES (%s, 'VAN', %s, %s, %s, %s, %s)
            """,
            (fl_id, body.fl_vehicle_brand, body.fl_vehicle_model,
             body.fl_vehicle_year, body.fl_vehicle_seat_capa, body.fl_vehicle_license_plate)
        )
        vehicle_id = cursor.lastrowid
        conn.commit()
        return {
            "fl_vehicle_id": vehicle_id,
            "fl_id": fl_id,
            "fl_vehicle_type": "VAN",
            "fl_vehicle_brand": body.fl_vehicle_brand,
            "fl_vehicle_model": body.fl_vehicle_model,
            "fl_vehicle_year": body.fl_vehicle_year,
            "fl_vehicle_seat_capa": body.fl_vehicle_seat_capa,
            "fl_vehicle_license_plate": body.fl_vehicle_license_plate,
        }
    except HTTPException:
        raise
    except Exception as e:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()


@router.delete("/fl-vehicle/{vehicle_id}/images/{image_id}")
def delete_fl_vehicle_image(vehicle_id: str, image_id: str):
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute(
            "SELECT fl_vehicle_image_id FROM fl_vehicle_images WHERE fl_vehicle_image_id = %s AND fl_vehicle_id = %s",
            (image_id, vehicle_id)
        )
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Image not found.")
        cursor.execute(
            "DELETE FROM fl_vehicle_images WHERE fl_vehicle_image_id = %s",
            (image_id,)
        )
        conn.commit()
        return {"success": True}
    except HTTPException:
        raise
    except Exception as e:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()

@router.post("/fl-availability")
def create_fl_availability(body: dict = Body(...)):
    conn = None
    try:
        fl_id = body.get("fl_id")
        start = body.get("fl_available_start_date")
        end = body.get("fl_available_end_date")
        if not fl_id or not start or not end:
            raise HTTPException(status_code=400, detail="fl_id, start_date, end_date required.")
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute("SELECT fl_available_id FROM fl_availability WHERE fl_id = %s", (fl_id,))
        existing = cursor.fetchone()
        if existing:
            cursor.execute(
                """UPDATE fl_availability
                   SET fl_available_start_date=%s, fl_available_end_date=%s, is_active=TRUE, updated_at=NOW()
                   WHERE fl_id=%s""",
                (start, end, fl_id)
            )
        else:
            cursor.execute(
                """INSERT INTO fl_availability (fl_id, fl_available_start_date, fl_available_end_date, is_active)
                   VALUES (%s, %s, %s, TRUE)""",
                (fl_id, start, end)
            )
        conn.commit()
        cursor.execute(
            """SELECT fl_available_id, fl_id, fl_available_start_date, fl_available_end_date, is_active, updated_at
               FROM fl_availability WHERE fl_id=%s""", (fl_id,)
        )
        return cursor.fetchone()
    except HTTPException:
        raise
    except Exception as e:
        if conn: conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn: conn.close()


@router.patch("/fl-availability/{fl_id}/toggle")
def toggle_fl_availability(fl_id: int):
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute("SELECT fl_available_id, is_active FROM fl_availability WHERE fl_id=%s", (fl_id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="No availability record found.")
        new_status = not row["is_active"]
        cursor.execute(
            "UPDATE fl_availability SET is_active=%s, updated_at=NOW() WHERE fl_id=%s",
            (new_status, fl_id)
        )
        conn.commit()
        return {"fl_id": fl_id, "is_active": new_status}
    except HTTPException:
        raise
    except Exception as e:
        if conn: conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn: conn.close()