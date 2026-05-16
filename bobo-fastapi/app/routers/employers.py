from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.db.connection import get_connection, get_cursor
import bcrypt

router = APIRouter(tags=["employers"])


class BanRequest(BaseModel):
    is_active: bool
    admin_id: str


class DocReviewRequest(BaseModel):
    status: str
    reviewed_by: str


class ProfileUpdateRequest(BaseModel):
    em_name: str
    em_email: str
    em_phone: Optional[str] = None
    em_address: Optional[str] = None
    em_bio: Optional[str] = None


class PasswordChangeRequest(BaseModel):
    current_password: str
    new_password: str


@router.get("/employers")
@router.get("/admin/employers")
def get_employers(limit: int = 50, offset: int = 0):
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute(
            """
            SELECT em_id, em_username, em_name, em_phone, em_email, em_address, em_bio,
                em_profile_image_url, em_verify_status, em_is_active,
                em_rating_avg, em_created_at, em_updated_at
            FROM employers
            ORDER BY em_updated_at DESC
            LIMIT %s OFFSET %s
            """,
            (limit, offset)
        )
        rows = cursor.fetchall()
        conn.close()
        return {"items": rows, "limit": limit, "offset": offset}
    except Exception as e:
        return {"error": str(e), "items": []}


@router.get("/employers/{em_id}")
def get_employer(em_id: str):
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute(
            """
            SELECT em_id, em_username, em_name, em_phone, em_email, em_address, em_bio,
                em_profile_image_url, em_verify_status, em_is_active,
                em_rating_avg, em_created_at, em_updated_at
            FROM employers
            WHERE em_id = %s
            """,
            (em_id,)
        )
        row = cursor.fetchone()
        conn.close()
        if not row:
            raise HTTPException(status_code=404, detail="Employer not found")
        return row
    except HTTPException:
        raise
    except Exception as e:
        return {"error": str(e)}


@router.put("/employers/{em_id}")
def update_employer(em_id: str, body: ProfileUpdateRequest):
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute("SELECT em_id FROM employers WHERE em_id = %s", (em_id,))
        if not cursor.fetchone():
            conn.close()
            raise HTTPException(status_code=404, detail="Employer not found")
        cursor.execute(
            """
            UPDATE employers
            SET em_name = %s, em_email = %s, em_phone = %s, em_address = %s, em_bio = %s, em_updated_at = NOW()
            WHERE em_id = %s
            """,
            (body.em_name, body.em_email, body.em_phone, body.em_address, body.em_bio, em_id)
        )
        conn.commit()
        conn.close()
        return {"status": "updated"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/employers/{em_id}/password")
def change_password(em_id: str, body: PasswordChangeRequest):
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute("SELECT em_password_hash FROM employers WHERE em_id = %s", (em_id,))
        employer = cursor.fetchone()
        if not employer:
            conn.close()
            raise HTTPException(status_code=404, detail="Employer not found")
        if not bcrypt.checkpw(body.current_password.encode(), employer["em_password_hash"].encode()):
            conn.close()
            raise HTTPException(status_code=401, detail="Current password is incorrect.")
        new_hash = bcrypt.hashpw(body.new_password.encode(), bcrypt.gensalt()).decode()
        cursor.execute(
            "UPDATE employers SET em_password_hash = %s WHERE em_id = %s",
            (new_hash, em_id)
        )
        conn.commit()
        conn.close()
        return {"status": "password updated"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/employers/{em_id}/ban")
def ban_employer(em_id: str, body: BanRequest):
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute("SELECT em_id FROM employers WHERE em_id = %s", (em_id,))
        if not cursor.fetchone():
            conn.close()
            raise HTTPException(status_code=404, detail="Employer not found")
        cursor.execute(
            "UPDATE employers SET em_is_active = %s WHERE em_id = %s",
            (body.is_active, em_id)
        )
        cursor.execute("SELECT em_name FROM employers WHERE em_id = %s", (em_id,))
        em_info = cursor.fetchone()
        action = 'UNBAN_USER' if body.is_active else 'BAN_USER'
        cursor.execute(
            """
            INSERT INTO admin_logs (admin_id, action_type, target_type, target_id, target_name, note)
            VALUES (%s, %s, 'EMPLOYER', %s, %s, NULL)
            """,
            (body.admin_id, action, em_id, em_info["em_name"] if em_info else em_id)
        )
        conn.commit()
        conn.close()
        return {"status": "updated", "em_id": em_id, "is_active": body.is_active}
    except HTTPException:
        raise
    except Exception as e:
        return {"error": str(e)}


@router.get("/em-documents")
def get_em_documents(limit: int = 50, offset: int = 0):
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute(
            """
            SELECT ed.em_doc_id, ed.em_id, e.em_name,
                   ed.em_doc_type, ed.file_url, ed.em_doc_status,
                   ed.is_latest, ed.em_uploaded_at,
                   a.name AS reviewed_by_name, ed.reviewed_at
            FROM em_documents ed
            JOIN employers e ON ed.em_id = e.em_id
            LEFT JOIN admins a ON ed.reviewed_by = a.admin_id
            ORDER BY ed.em_uploaded_at DESC
            LIMIT %s OFFSET %s
            """,
            (limit, offset)
        )
        rows = cursor.fetchall()
        conn.close()
        return {"items": rows, "limit": limit, "offset": offset}
    except Exception as e:
        return {"error": str(e), "items": []}


@router.get("/em-verification")
def get_em_verification(limit: int = 50, offset: int = 0):
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute(
            """
            SELECT ev.em_verify_id, ev.em_id, e.em_name,
                   ev.em_verify_status, ev.em_submitted_at, ev.em_verified_at,
                   a.name AS reviewed_by_name
            FROM em_verification ev
            JOIN employers e ON ev.em_id = e.em_id
            LEFT JOIN admins a ON ev.reviewed_by = a.admin_id
            ORDER BY ev.em_submitted_at DESC
            LIMIT %s OFFSET %s
            """,
            (limit, offset)
        )
        rows = cursor.fetchall()
        conn.close()
        return {"items": rows, "limit": limit, "offset": offset}
    except Exception as e:
        return {"error": str(e), "items": []}


@router.patch("/em-documents/{doc_id}")
def review_em_document(doc_id: str, body: DocReviewRequest):
    if body.status not in ("APPROVED", "REJECTED"):
        raise HTTPException(status_code=400, detail="status must be APPROVED or REJECTED")
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute("SELECT em_doc_id, em_id FROM em_documents WHERE em_doc_id = %s", (doc_id,))
        doc = cursor.fetchone()
        if not doc:
            conn.close()
            raise HTTPException(status_code=404, detail="Document not found")
        cursor.execute(
            """
            UPDATE em_documents
            SET em_doc_status = %s, reviewed_by = %s, reviewed_at = NOW()
            WHERE em_doc_id = %s
            """,
            (body.status, body.reviewed_by, doc_id)
        )
        if body.status == "APPROVED":
            cursor.execute(
                "SELECT COUNT(*) AS c FROM em_documents WHERE em_id = %s AND is_latest = 1 AND em_doc_status != 'APPROVED'",
                (doc["em_id"],)
            )
            remaining = cursor.fetchone()["c"]
            if remaining == 0:
                cursor.execute("UPDATE employers SET em_verify_status = 'VERIFIED' WHERE em_id = %s", (doc["em_id"],))
                cursor.execute(
                    "UPDATE em_verification SET em_verify_status = 'VERIFIED', em_verified_at = NOW(), reviewed_by = %s WHERE em_id = %s AND is_latest = 1",
                    (body.reviewed_by, doc["em_id"])
                )
        elif body.status == "REJECTED":
            cursor.execute("UPDATE employers SET em_verify_status = 'NOT_VERIFIED' WHERE em_id = %s", (doc["em_id"],))
            cursor.execute("UPDATE em_verification SET em_verify_status = 'NOT_VERIFIED' WHERE em_id = %s AND is_latest = 1", (doc["em_id"],))

        cursor.execute(
            "SELECT e.em_name, ed.em_doc_type FROM em_documents ed JOIN employers e ON ed.em_id = e.em_id WHERE ed.em_doc_id = %s",
            (doc_id,)
        )
        doc_info = cursor.fetchone()
        if doc_info:
            action = 'APPROVE_DOCUMENT' if body.status == 'APPROVED' else 'REJECT_DOCUMENT'
            cursor.execute(
                "INSERT INTO admin_logs (admin_id, action_type, target_type, target_id, target_name, note) VALUES (%s, %s, 'DOCUMENT', %s, %s, %s)",
                (body.reviewed_by, action, doc_id, doc_info["em_name"], doc_info["em_doc_type"])
            )
            if body.status == "APPROVED":
                cursor.execute(
                    "SELECT COUNT(*) AS c FROM em_documents WHERE em_id = %s AND is_latest = 1 AND em_doc_status != 'APPROVED'",
                    (doc["em_id"],)
                )
                if cursor.fetchone()["c"] == 0:
                    cursor.execute("SELECT em_name FROM employers WHERE em_id = %s", (doc["em_id"],))
                    em_info = cursor.fetchone()
                    cursor.execute(
                        "INSERT INTO admin_logs (admin_id, action_type, target_type, target_id, target_name, note) VALUES (%s, 'VERIFY_EMPLOYER', 'EMPLOYER', %s, %s, 'All 5 documents approved')",
                        (body.reviewed_by, doc["em_id"], em_info["em_name"])
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
