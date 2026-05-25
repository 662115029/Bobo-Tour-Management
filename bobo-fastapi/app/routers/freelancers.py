from fastapi import APIRouter, HTTPException
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
def get_fl_bank_accounts(limit: int = 10, offset: int = 0):
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute(
            """
            SELECT fb.fl_bank_account_id, fb.fl_id, f.fl_name,
                   fb.account_name, fb.account_number, fb.bank_name,
                   fb.is_primary, fb.created_at, fb.updated_at
            FROM fl_bank_accounts fb
            JOIN freelancers f ON fb.fl_id = f.fl_id
            ORDER BY fb.created_at DESC
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
@router.get("/fl-vehicle")
def get_fl_vehicle(limit: int = 10, offset: int = 0):
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute(
            """
            SELECT fv.fl_vehicle_id, fv.fl_id, f.fl_name,
                   fv.fl_vehicle_type, fv.fl_vehicle_brand, fv.fl_vehicle_model,
                   fv.fl_vehicle_year, fv.fl_vehicle_seat_capa,
                   fv.fl_vehicle_license_plate,
                   fv.fl_vehicle_created_at, fv.fl_vehicle_updated_at
            FROM fl_vehicle fv
            JOIN freelancers f ON fv.fl_id = f.fl_id
            ORDER BY fv.fl_vehicle_created_at DESC
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
@router.get("/fl-vehicle-images")
def get_fl_vehicle_images(limit: int = 10, offset: int = 0):
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute(
            """
            SELECT fvi.fl_vehicle_image_id, fvi.fl_vehicle_id,
                   fv.fl_vehicle_brand, fv.fl_vehicle_model,
                   fv.fl_vehicle_license_plate, f.fl_name,
                   fvi.fl_vehicle_image_url, fvi.uploaded_at
            FROM fl_vehicle_images fvi
            JOIN fl_vehicle fv ON fvi.fl_vehicle_id = fv.fl_vehicle_id
            JOIN freelancers f ON fv.fl_id = f.fl_id
            ORDER BY fvi.uploaded_at DESC
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
@router.get("/fl-languages")
def get_fl_languages(limit: int = 10, offset: int = 0):
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute(
            """
            SELECT fl.fl_id, f.fl_name,
                   l.language_id, l.language_name
            FROM fl_languages fl
            JOIN freelancers f ON fl.fl_id = f.fl_id
            JOIN languages l ON fl.language_id = l.language_id
            ORDER BY f.fl_name, l.language_name
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
@router.get("/fl-pickup-areas")
def get_fl_pickup_areas(limit: int = 10, offset: int = 0):
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute(
            """
            SELECT fp.fl_id, f.fl_name,
                   a.area_id, a.area_name
            FROM fl_pickup_areas fp
            JOIN freelancers f ON fp.fl_id = f.fl_id
            JOIN areas a ON fp.area_id = a.area_id
            ORDER BY f.fl_name, a.area_name
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
@router.get("/fl-availability")
def get_fl_availability(limit: int = 10, offset: int = 0):
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute(
            """
            SELECT fa.fl_available_id, fa.fl_id, f.fl_name,
                   fa.fl_available_start_date, fa.fl_available_end_date,
                   fa.is_active, fa.created_at, fa.updated_at
            FROM fl_availability fa
            JOIN freelancers f ON fa.fl_id = f.fl_id
            ORDER BY fa.fl_available_start_date DESC
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
@router.get("/fl-documents")
def get_fl_documents(limit: int = 10, offset: int = 0, status: str = "", fl_ids: str = ""):
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        where = []
        params = []
        if fl_ids:
            id_list = [int(i) for i in fl_ids.split(',') if i.strip().isdigit()]
            placeholders = ','.join(['%s'] * len(id_list))
            where.append(f"fd.fl_id IN ({placeholders})")
            params += id_list
        if status:
            where.append("fd.fl_doc_status = %s")
            params.append(status)
        elif not fl_ids:
            where.append("fd.file_url IS NOT NULL")
        where_sql = "WHERE " + " AND ".join(where) if where else ""
        params += [limit, offset]
        cursor.execute(
            f"""
            SELECT fd.fl_doc_id, fd.fl_id, f.fl_name,
                   fd.fl_doc_type, fd.file_url, fd.fl_doc_status,
                   fd.fl_uploaded_at,
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
def get_fl_verification(limit: int = 10, offset: int = 0, status: str = "PENDING"):
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        where_sql = "WHERE fv.fl_verify_status = %s" if status else ""
        params = ([status] if status else []) + [limit, offset]
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
    if body.status not in ("APPROVED", "REJECTED"):
        raise HTTPException(status_code=400, detail="status must be APPROVED or REJECTED")
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute("SELECT fl_doc_id, fl_id FROM fl_documents WHERE fl_doc_id = %s", (doc_id,))
        doc = cursor.fetchone()
        if not doc:
            raise HTTPException(status_code=404, detail="Document not found")

        cursor.execute(
            """
            UPDATE fl_documents
            SET fl_doc_status = %s, reviewed_by = %s, reviewed_at = NOW()
            WHERE fl_doc_id = %s
            """,
            (body.status, body.reviewed_by, doc_id)
        )

        if body.status == "APPROVED":
            cursor.execute(
                """
                SELECT COUNT(*) AS c FROM fl_documents
                WHERE fl_id = %s AND fl_doc_status != 'APPROVED'
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
        elif body.status == "REJECTED":
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
            action = 'APPROVE_DOCUMENT' if body.status == 'APPROVED' else 'REJECT_DOCUMENT'
            cursor.execute(
                """
                INSERT INTO admin_logs
                    (admin_id, action_type, target_type, target_id, target_name, note)
                VALUES (%s, %s, 'DOCUMENT', %s, %s, %s)
                """,
                (body.reviewed_by, action, doc_id,
                 doc_info["fl_name"], doc_info["fl_doc_type"])
            )
            if body.status == "APPROVED":
                cursor.execute(
                    "SELECT COUNT(*) AS c FROM fl_documents WHERE fl_id = %s AND fl_doc_status != 'APPROVED'",
                    (doc["fl_id"],)
                )
                if cursor.fetchone()["c"] == 0:
                    cursor.execute("SELECT fl_name FROM freelancers WHERE fl_id = %s", (doc["fl_id"],))
                    fl_info = cursor.fetchone()
                    cursor.execute(
                        """
                        INSERT INTO admin_logs
                            (admin_id, action_type, target_type, target_id, target_name, note)
                        VALUES (%s, 'VERIFY_FREELANCER', 'FREELANCER', %s, %s, 'All 5 documents approved')
                        """,
                        (body.reviewed_by, doc["fl_id"], fl_info["fl_name"])
                    )

        conn.commit()
        return {"status": "updated", "doc_id": doc_id, "new_status": body.status}
    except HTTPException:
        raise
    except Exception as e:
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