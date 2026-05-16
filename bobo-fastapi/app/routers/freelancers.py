from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.db.connection import get_connection, get_cursor

router = APIRouter(tags=["freelancers"])


class BanRequest(BaseModel):
    is_active: bool
    admin_id: str


class DocReviewRequest(BaseModel):
    status: str
    reviewed_by: str


@router.get("/freelancers")
@router.get("/admin/freelancers")
def get_freelancers(limit: int = 50, offset: int = 0):
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute(
            """
            SELECT fl_id, line_user_id, fl_name, fl_date_of_birth,
                   fl_address, fl_bio, fl_profile_image_url,
                   fl_verify_status, fl_is_active, fl_rating_avg,
                   fl_created_at, fl_updated_at
            FROM freelancers
            ORDER BY fl_updated_at DESC
            LIMIT %s OFFSET %s
            """,
            (limit, offset)
        )
        rows = cursor.fetchall()
        conn.close()
        return {"items": rows, "limit": limit, "offset": offset}
    except Exception as e:
        return {"error": str(e), "items": []}


@router.get("/freelancers/{fl_id}")
def get_freelancer(fl_id: str):
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute(
            """
            SELECT fl_id, line_user_id, fl_name, fl_date_of_birth,
                   fl_address, fl_bio, fl_profile_image_url,
                   fl_verify_status, fl_is_active, fl_rating_avg,
                   fl_created_at, fl_updated_at
            FROM freelancers WHERE fl_id = %s
            """,
            (fl_id,)
        )
        row = cursor.fetchone()
        conn.close()
        if not row:
            raise HTTPException(status_code=404, detail="Freelancer not found")
        return row
    except HTTPException:
        raise
    except Exception as e:
        return {"error": str(e)}


@router.get("/fl-vehicle")
def get_fl_vehicle(limit: int = 50, offset: int = 0):
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute(
            """
            SELECT fv.fl_vehicle_id, fv.fl_id, f.fl_name,
                   fv.fl_vehicle_type, fv.fl_vehicle_brand, fv.fl_vehicle_model,
                   fv.fl_vehicle_year, fv.fl_vehicle_seat_capa, fv.fl_vehicle_license_plate
            FROM fl_vehicle fv
            JOIN freelancers f ON fv.fl_id = f.fl_id
            ORDER BY fv.fl_id
            LIMIT %s OFFSET %s
            """,
            (limit, offset)
        )
        rows = cursor.fetchall()
        conn.close()
        return {"items": rows, "limit": limit, "offset": offset}
    except Exception as e:
        return {"error": str(e), "items": []}


@router.get("/fl-vehicle-images")
def get_fl_vehicle_images(limit: int = 50, offset: int = 0):
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute(
            """
            SELECT fvi.fl_vehicle_image_id, fvi.fl_vehicle_id,
                   fv.fl_vehicle_brand, fv.fl_vehicle_model,
                   fv.fl_vehicle_license_plate, f.fl_name,
                   fvi.fl_vehicle_image_url
            FROM fl_vehicle_images fvi
            JOIN fl_vehicle fv ON fvi.fl_vehicle_id = fv.fl_vehicle_id
            JOIN freelancers f ON fv.fl_id = f.fl_id
            LIMIT %s OFFSET %s
            """,
            (limit, offset)
        )
        rows = cursor.fetchall()
        conn.close()
        return {"items": rows, "limit": limit, "offset": offset}
    except Exception as e:
        return {"error": str(e), "items": []}


@router.get("/fl-languages")
def get_fl_languages(limit: int = 50, offset: int = 0):
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute(
            """
            SELECT fl.fl_language_id, fl.fl_id, f.fl_name, fl.fl_language_name
            FROM fl_languages fl
            JOIN freelancers f ON fl.fl_id = f.fl_id
            ORDER BY f.fl_name, fl.fl_language_name
            LIMIT %s OFFSET %s
            """,
            (limit, offset)
        )
        rows = cursor.fetchall()
        conn.close()
        return {"items": rows, "limit": limit, "offset": offset}
    except Exception as e:
        return {"error": str(e), "items": []}


@router.get("/fl-pickup-areas")
def get_fl_pickup_areas(limit: int = 50, offset: int = 0):
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute(
            """
            SELECT fp.fl_area_id, fp.fl_id, f.fl_name, fp.fl_area_name
            FROM fl_pickup_areas fp
            JOIN freelancers f ON fp.fl_id = f.fl_id
            ORDER BY f.fl_name, fp.fl_area_name
            LIMIT %s OFFSET %s
            """,
            (limit, offset)
        )
        rows = cursor.fetchall()
        conn.close()
        return {"items": rows, "limit": limit, "offset": offset}
    except Exception as e:
        return {"error": str(e), "items": []}


@router.get("/fl-availability")
def get_fl_availability(limit: int = 50, offset: int = 0):
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute(
            """
            SELECT fa.fl_available_id, fa.fl_id, f.fl_name,
                   fa.fl_available_start_date, fa.fl_available_end_date, fa.is_active
            FROM fl_availability fa
            JOIN freelancers f ON fa.fl_id = f.fl_id
            ORDER BY fa.fl_available_start_date DESC
            LIMIT %s OFFSET %s
            """,
            (limit, offset)
        )
        rows = cursor.fetchall()
        conn.close()
        return {"items": rows, "limit": limit, "offset": offset}
    except Exception as e:
        return {"error": str(e), "items": []}


@router.get("/fl-documents")
def get_fl_documents(limit: int = 50, offset: int = 0):
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute(
            """
            SELECT fd.fl_doc_id, fd.fl_id, f.fl_name,
                   fd.fl_doc_type, fd.file_url, fd.fl_doc_status,
                   fd.is_latest, fd.fl_uploaded_at,
                   a.name AS reviewed_by_name, fd.reviewed_at
            FROM fl_documents fd
            JOIN freelancers f ON fd.fl_id = f.fl_id
            LEFT JOIN admins a ON fd.reviewed_by = a.admin_id
            ORDER BY fd.fl_uploaded_at DESC
            LIMIT %s OFFSET %s
            """,
            (limit, offset)
        )
        rows = cursor.fetchall()
        conn.close()
        return {"items": rows, "limit": limit, "offset": offset}
    except Exception as e:
        return {"error": str(e), "items": []}


@router.get("/fl-verification")
def get_fl_verification(limit: int = 50, offset: int = 0):
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute(
            """
            SELECT fv.fl_verify_id, fv.fl_id, f.fl_name,
                   fv.fl_verify_status, fv.fl_submitted_at, fv.fl_verified_at,
                   a.name AS reviewed_by_name
            FROM fl_verification fv
            JOIN freelancers f ON fv.fl_id = f.fl_id
            LEFT JOIN admins a ON fv.reviewed_by = a.admin_id
            ORDER BY fv.fl_submitted_at DESC
            LIMIT %s OFFSET %s
            """,
            (limit, offset)
        )
        rows = cursor.fetchall()
        conn.close()
        return {"items": rows, "limit": limit, "offset": offset}
    except Exception as e:
        return {"error": str(e), "items": []}


@router.patch("/freelancers/{fl_id}/ban")
def ban_freelancer(fl_id: str, body: BanRequest):
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute("SELECT fl_id FROM freelancers WHERE fl_id = %s", (fl_id,))
        if not cursor.fetchone():
            conn.close()
            raise HTTPException(status_code=404, detail="Freelancer not found")
        cursor.execute("UPDATE freelancers SET fl_is_active = %s WHERE fl_id = %s", (body.is_active, fl_id))
        cursor.execute("SELECT fl_name FROM freelancers WHERE fl_id = %s", (fl_id,))
        fl_info = cursor.fetchone()
        action = 'UNBAN_USER' if body.is_active else 'BAN_USER'
        cursor.execute(
            "INSERT INTO admin_logs (admin_id, action_type, target_type, target_id, target_name, note) VALUES (%s, %s, 'FREELANCER', %s, %s, NULL)",
            (body.admin_id, action, fl_id, fl_info["fl_name"] if fl_info else fl_id)
        )
        conn.commit()
        conn.close()
        return {"status": "updated", "fl_id": fl_id, "is_active": body.is_active}
    except HTTPException:
        raise
    except Exception as e:
        return {"error": str(e)}


@router.patch("/fl-documents/{doc_id}")
def review_fl_document(doc_id: str, body: DocReviewRequest):
    if body.status not in ("APPROVED", "REJECTED"):
        raise HTTPException(status_code=400, detail="status must be APPROVED or REJECTED")
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute("SELECT fl_doc_id, fl_id FROM fl_documents WHERE fl_doc_id = %s", (doc_id,))
        doc = cursor.fetchone()
        if not doc:
            conn.close()
            raise HTTPException(status_code=404, detail="Document not found")
        cursor.execute(
            "UPDATE fl_documents SET fl_doc_status = %s, reviewed_by = %s, reviewed_at = NOW() WHERE fl_doc_id = %s",
            (body.status, body.reviewed_by, doc_id)
        )
        if body.status == "APPROVED":
            cursor.execute(
                "SELECT COUNT(*) AS c FROM fl_documents WHERE fl_id = %s AND is_latest = 1 AND fl_doc_status != 'APPROVED'",
                (doc["fl_id"],)
            )
            if cursor.fetchone()["c"] == 0:
                cursor.execute("UPDATE freelancers SET fl_verify_status = 'VERIFIED' WHERE fl_id = %s", (doc["fl_id"],))
                cursor.execute(
                    "UPDATE fl_verification SET fl_verify_status = 'VERIFIED', fl_verified_at = NOW(), reviewed_by = %s WHERE fl_id = %s AND is_latest = 1",
                    (body.reviewed_by, doc["fl_id"])
                )
        elif body.status == "REJECTED":
            cursor.execute("UPDATE freelancers SET fl_verify_status = 'NOT_VERIFIED' WHERE fl_id = %s", (doc["fl_id"],))
            cursor.execute("UPDATE fl_verification SET fl_verify_status = 'NOT_VERIFIED' WHERE fl_id = %s AND is_latest = 1", (doc["fl_id"],))

        cursor.execute(
            "SELECT f.fl_name, fd.fl_doc_type FROM fl_documents fd JOIN freelancers f ON fd.fl_id = f.fl_id WHERE fd.fl_doc_id = %s",
            (doc_id,)
        )
        doc_info = cursor.fetchone()
        if doc_info:
            action = 'APPROVE_DOCUMENT' if body.status == 'APPROVED' else 'REJECT_DOCUMENT'
            cursor.execute(
                "INSERT INTO admin_logs (admin_id, action_type, target_type, target_id, target_name, note) VALUES (%s, %s, 'DOCUMENT', %s, %s, %s)",
                (body.reviewed_by, action, doc_id, doc_info["fl_name"], doc_info["fl_doc_type"])
            )
            if body.status == "APPROVED":
                cursor.execute(
                    "SELECT COUNT(*) AS c FROM fl_documents WHERE fl_id = %s AND is_latest = 1 AND fl_doc_status != 'APPROVED'",
                    (doc["fl_id"],)
                )
                if cursor.fetchone()["c"] == 0:
                    cursor.execute("SELECT fl_name FROM freelancers WHERE fl_id = %s", (doc["fl_id"],))
                    fl_info = cursor.fetchone()
                    cursor.execute(
                        "INSERT INTO admin_logs (admin_id, action_type, target_type, target_id, target_name, note) VALUES (%s, 'VERIFY_FREELANCER', 'FREELANCER', %s, %s, 'All 5 documents approved')",
                        (body.reviewed_by, doc["fl_id"], fl_info["fl_name"])
                    )
        conn.commit()
        conn.close()
        return {"status": "updated", "doc_id": doc_id, "new_status": body.status}
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        conn.close()
        return {"error": str(e)}
