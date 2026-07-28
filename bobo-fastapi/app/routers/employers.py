from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.db.connection import get_connection, get_cursor
from .utils import (
    validate_password,
    validate_doc_review_status,
    determine_verify_status,
    sanitize_sort_params,
    validate_profile_update_fields,
)
import bcrypt

router = APIRouter(tags=["employers"])

EM_DOC_TYPES = [
    "COMPANY_REGISTRATION",
    "BUSINESS_LICENSE",
    "TOURISM_LICENSE",
    "TAX_ID_DOCUMENT",
    "AUTHORIZED_PERSON_ID",
]


class EmployerRegisterRequest(BaseModel):
    em_username: str
    em_email: str
    em_name: str
    em_phone: str
    em_password: str


class DocReviewRequest(BaseModel):
    status: str
    reviewed_by: str
    note: Optional[str] = None
    reason: Optional[str] = None


class BanRequest(BaseModel):
    is_active: bool
    admin_id: str


class ProfileUpdateRequest(BaseModel):
    em_name: Optional[str] = None
    em_email: Optional[str] = None
    em_phone: Optional[str] = None
    em_address: Optional[str] = None
    em_bio: Optional[str] = None
    em_profile_image_url: Optional[str] = None
    job_templates: Optional[str] = None


_EMPLOYER_NOT_FOUND = "Employer not found"

@router.put("/employers/{em_id}")
def update_employer(em_id: str, body: ProfileUpdateRequest):
    conn = None
    try:
        fields = {k: v for k, v in {
            "em_name": body.em_name,
            "em_email": body.em_email,
            "em_phone": body.em_phone,
            "em_address": body.em_address,
            "em_bio": body.em_bio,
        }.items() if v is not None}

        fields_err = validate_profile_update_fields(fields)
        if fields_err:
            raise HTTPException(status_code=400, detail=fields_err)

        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute("SELECT em_id FROM employers WHERE em_id = %s", (em_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail=_EMPLOYER_NOT_FOUND)
        cursor.execute(
            """
            UPDATE employers
            SET em_name = %s, em_email = %s, em_phone = %s, em_address = %s, em_bio = %s,
                em_profile_image_url = COALESCE(%s, em_profile_image_url),
                job_templates = COALESCE(%s, job_templates)
            WHERE em_id = %s
            """,
            (body.em_name, body.em_email, body.em_phone, body.em_address, body.em_bio,
             body.em_profile_image_url, body.job_templates, em_id)
        )
        conn.commit()
        return {"status": "updated"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()


@router.get("/employers")
@router.get("/admin/employers")
def get_employers(limit: int = 10, offset: int = 0, search: str = "", status: str = "", sort_by: str = "em_updated_at", sort_order: str = "desc"):
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        where = []
        params = []
        if search:
            where.append("(em_name LIKE %s OR em_username LIKE %s)")
            params += [f"%{search}%", f"%{search}%"]
        if status:
            where.append("em_verify_status = %s")
            params.append(status)
        where_sql = "WHERE " + " AND ".join(where) if where else ""
        params += [limit, offset]
        allowed_sort = {"em_name", "em_rating_avg", "em_updated_at", "em_created_at"}
        safe_sort_by, safe_order = sanitize_sort_params(sort_by, sort_order, allowed_sort, "em_updated_at")
        cursor.execute(
            f"""
            SELECT em_id, em_username, em_email, em_name, em_phone, em_address, em_bio,
                   em_profile_image_url, em_verify_status, em_is_active, job_templates,
                   em_rating_avg, em_created_at, em_updated_at
            FROM employers
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


@router.get("/employers/{em_id}")
def get_employer(em_id: str):
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute(
            """
            SELECT em_id, em_username, em_email, em_name, em_phone, em_address, em_bio,
                   em_profile_image_url, em_verify_status, em_is_active, job_templates,
                   em_rating_avg, em_created_at, em_updated_at
            FROM employers
            WHERE em_id = %s
            """,
            (em_id,)
        )
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Employer not found")
        return row
    except HTTPException:
        raise
    except Exception as e:
        return {"error": str(e)}
    finally:
        if conn:
            conn.close()


@router.post("/employers/{em_id}/verify-password")
def verify_employer_password(em_id: int, data: dict):
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute(
            "SELECT em_password_hash FROM employers WHERE em_id = %s",
            (em_id,)
        )
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail=_EMPLOYER_NOT_FOUND)

        current_password = data.get("current_password", "")
        if not bcrypt.checkpw(current_password.encode(), row["em_password_hash"].encode()):
            raise HTTPException(status_code=401, detail="Incorrect password.")

        return {"success": True}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()



@router.post("/employers/{em_id}/resubmit-verification")
def resubmit_verification(em_id: int):
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute("SELECT em_id FROM employers WHERE em_id = %s", (em_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail=_EMPLOYER_NOT_FOUND)
        # Set old verification records to not latest
        cursor.execute(
            "UPDATE em_verification SET is_latest = FALSE WHERE em_id = %s",
            (em_id,)
        )
        # Insert new PENDING verification record
        cursor.execute(
            """
            INSERT INTO em_verification (em_id, em_verify_status, is_latest, em_submitted_at)
            VALUES (%s, 'PENDING', TRUE, NOW())
            """,
            (em_id,)
        )
        # Reset employer status
        cursor.execute(
            "UPDATE employers SET em_verify_status = 'PENDING' WHERE em_id = %s",
            (em_id,)
        )
        conn.commit()
        return {"success": True, "em_verify_status": "PENDING"}
    except HTTPException:
        raise
    except Exception as e:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()


@router.put("/employers/{em_id}/password")
def change_employer_password(em_id: int, data: dict):
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute(
            "SELECT em_password_hash FROM employers WHERE em_id = %s",
            (em_id,)
        )
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail=_EMPLOYER_NOT_FOUND)

        current_password = data.get("current_password", "")
        if not bcrypt.checkpw(current_password.encode(), row["em_password_hash"].encode()):
            raise HTTPException(status_code=401, detail="Incorrect current password.")

        new_password = data.get("new_password", "")
        pwd_err = validate_password(new_password, min_length=8)
        if pwd_err:
            raise HTTPException(status_code=400, detail=f"New password: {pwd_err}")

        new_hash = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
        cursor.execute(
            "UPDATE employers SET em_password_hash = %s WHERE em_id = %s",
            (new_hash, em_id)
        )
        conn.commit()
        return {"success": True, "message": "Password updated successfully."}
    except HTTPException:
        raise
    except Exception as e:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()


@router.get("/em-bank-accounts")
def get_em_bank_accounts(limit: int = 10, offset: int = 0, em_id: Optional[int] = None):
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        where_sql = "WHERE eb.em_id = %s" if em_id else ""
        params = ([em_id] if em_id else []) + [limit, offset]
        cursor.execute(
            f"""
            SELECT eb.em_bank_account_id, eb.em_id, e.em_name,
                   eb.account_name, eb.account_number, eb.bank_name,
                   eb.is_primary, eb.created_at, eb.updated_at
            FROM em_bank_accounts eb
            JOIN employers e ON eb.em_id = e.em_id
            {where_sql}
            ORDER BY eb.created_at DESC
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


@router.get("/em-documents")
def get_em_documents(limit: int = 10, offset: int = 0, status: str = "", em_id: Optional[int] = None, em_ids: str = ""):
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        where = []
        params = []
        if em_id:
            where.append("ed.em_id = %s")
            params.append(em_id)
        elif em_ids:
            id_list = [int(i) for i in em_ids.split(',') if i.strip().isdigit()]
            placeholders = ','.join(['%s'] * len(id_list))
            where.append(f"ed.em_id IN ({placeholders})")
            params += id_list
        if status:
            where.append("ed.em_doc_status = %s")
            params.append(status)
        elif not em_id and not em_ids:
            where.append("ed.file_url IS NOT NULL")
        where_sql = "WHERE " + " AND ".join(where) if where else ""
        params += [limit, offset]
        cursor.execute(
            f"""
            SELECT ed.em_doc_id, ed.em_id, e.em_name,
                   ed.em_doc_type, ed.file_url, ed.em_doc_status,
                   ed.em_uploaded_at, ed.reject_reason,
                   a.name AS reviewed_by_name, ed.reviewed_at
            FROM em_documents ed
            JOIN employers e ON ed.em_id = e.em_id
            LEFT JOIN admins a ON ed.reviewed_by = a.admin_id
            {where_sql}
            ORDER BY ed.em_uploaded_at ASC
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


@router.get("/em-verification")
def get_em_verification(limit: int = 10, offset: int = 0, status: str = "", em_id: Optional[int] = None, is_latest: Optional[bool] = None):
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        where = []
        params = []
        if em_id:
            where.append("ev.em_id = %s")
            params.append(em_id)
        if status:
            where.append("ev.em_verify_status = %s")
            params.append(status)
        if is_latest is not None:
            where.append("ev.is_latest = %s")
            params.append(is_latest)
        where_sql = ("WHERE " + " AND ".join(where)) if where else ""
        params += [limit, offset]
        cursor.execute(
            f"""
            SELECT ev.em_verify_id, ev.em_id, e.em_name,
                   ev.em_verify_status, ev.is_latest,
                   ev.em_submitted_at, ev.em_verified_at,
                   a.name AS reviewed_by_name
            FROM em_verification ev
            JOIN employers e ON ev.em_id = e.em_id
            LEFT JOIN admins a ON ev.reviewed_by = a.admin_id
            {where_sql}
            ORDER BY ev.em_submitted_at DESC
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


@router.patch("/em-documents/{doc_id}")
@router.patch("/em-documents/{doc_id}")
def review_em_document(doc_id: str, body: DocReviewRequest):
    status_err = validate_doc_review_status(body.status)
    if status_err:
        raise HTTPException(status_code=400, detail=status_err)
    if body.status == "REJECTED" and not (body.reason or "").strip():
        raise HTTPException(status_code=400, detail="Rejection reason is required.")
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute("SELECT em_doc_id, em_id FROM em_documents WHERE em_doc_id = %s", (doc_id,))
        doc = cursor.fetchone()
        if not doc:
            raise HTTPException(status_code=404, detail="Document not found")

        reject_reason = body.reason if body.status == "REJECTED" else None
        cursor.execute(
            """
            UPDATE em_documents
            SET em_doc_status = %s, reviewed_by = %s, reviewed_at = NOW(),
                reject_reason = %s
            WHERE em_doc_id = %s
            """,
            (body.status, body.reviewed_by, reject_reason, doc_id)
        )

        if body.status == "APPROVED":
            cursor.execute(
                """
                SELECT
                  COUNT(*) AS total,
                  SUM(CASE WHEN em_doc_status = 'APPROVED' THEN 1 ELSE 0 END) AS approved,
                  SUM(CASE WHEN em_doc_status = 'PENDING'  THEN 1 ELSE 0 END) AS pending
                FROM em_documents
                WHERE em_id = %s AND file_url IS NOT NULL
                """,
                (doc["em_id"],)
            )
            counts = cursor.fetchone()
            new_status = determine_verify_status(
                counts["total"] or 0,
                counts["approved"] or 0,
                counts["pending"] or 0,
            )
            cursor.execute(
                "UPDATE employers SET em_verify_status = %s WHERE em_id = %s",
                (new_status, doc["em_id"])
            )
            if new_status == "VERIFIED":
                cursor.execute(
                    """
                    UPDATE em_verification SET em_verify_status = 'VERIFIED',
                    em_verified_at = NOW(), reviewed_by = %s
                    WHERE em_id = %s AND is_latest = 1
                    """,
                    (body.reviewed_by, doc["em_id"])
                )
        elif body.status == "REJECTED":
            cursor.execute(
                """
                SELECT
                  SUM(CASE WHEN em_doc_status = 'REJECTED' THEN 1 ELSE 0 END) AS rejected,
                  SUM(CASE WHEN em_doc_status = 'PENDING'  THEN 1 ELSE 0 END) AS pending,
                  SUM(CASE WHEN em_doc_status = 'APPROVED' THEN 1 ELSE 0 END) AS approved,
                  COUNT(*) AS total
                FROM em_documents
                WHERE em_id = %s AND file_url IS NOT NULL
                """,
                (doc["em_id"],)
            )
            counts = cursor.fetchone()
            new_status = determine_verify_status(
                counts["total"] or 0,
                counts["approved"] or 0,
                counts["pending"] or 0,
            )
            all_rejected = new_status == "NOT_VERIFIED"
            cursor.execute(
                "UPDATE employers SET em_verify_status = %s WHERE em_id = %s",
                (new_status, doc["em_id"])
            )
            if all_rejected:
                cursor.execute(
                    """
                    UPDATE em_verification SET em_verify_status = 'NOT_VERIFIED'
                    WHERE em_id = %s AND is_latest = 1
                    """,
                    (doc["em_id"],)
                )
            else:
                cursor.execute(
                    """
                    UPDATE em_verification SET em_verify_status = 'PENDING'
                    WHERE em_id = %s AND is_latest = 1
                    """,
                    (doc["em_id"],)
                )

        if body.status == "PENDING":
            cursor.execute(
                "UPDATE employers SET em_verify_status = 'PENDING' WHERE em_id = %s",
                (doc["em_id"],)
            )
            cursor.execute(
                """
                UPDATE em_verification SET em_verify_status = 'PENDING'
                WHERE em_id = %s AND is_latest = 1
                """,
                (doc["em_id"],)
            )

        cursor.execute(
            """
            SELECT e.em_name, ed.em_doc_type
            FROM em_documents ed
            JOIN employers e ON ed.em_id = e.em_id
            WHERE ed.em_doc_id = %s
            """,
            (doc_id,)
        )
        doc_info = cursor.fetchone()
        if doc_info:
            doc_label = doc_info["em_doc_type"].replace('_', ' ').title()
            if body.status == 'REJECTED':
                log_note = f"{doc_label}: {body.reason}" if body.reason else doc_label
                cursor.execute(
                    """
                    INSERT INTO admin_logs
                        (admin_id, action_type, target_type, target_id, target_name, note)
                    VALUES (%s, 'REJECT_DOCUMENT', 'DOCUMENT', %s, %s, %s)
                    """,
                    (body.reviewed_by, doc_id, doc_info["em_name"], log_note)
                )
                if all_rejected:
                    cursor.execute("SELECT em_name FROM employers WHERE em_id = %s", (doc["em_id"],))
                    em_info = cursor.fetchone()
                    cursor.execute(
                        """
                        INSERT INTO admin_logs
                            (admin_id, action_type, target_type, target_id, target_name, note)
                        VALUES (%s, 'NOT_VERIFY_EMPLOYER', 'EMPLOYER', %s, %s, 'All uploaded documents rejected')
                        """,
                        (body.reviewed_by, doc["em_id"], em_info["em_name"] if em_info else doc["em_id"])
                    )
            elif body.status == "APPROVED":
                cursor.execute(
                    """
                    INSERT INTO admin_logs
                        (admin_id, action_type, target_type, target_id, target_name, note)
                    VALUES (%s, 'APPROVE_DOCUMENT', 'DOCUMENT', %s, %s, %s)
                    """,
                    (body.reviewed_by, doc_id, doc_info["em_name"], doc_label)
                )
                cursor.execute(
                    "SELECT COUNT(*) AS c FROM em_documents WHERE em_id = %s AND em_doc_status != 'APPROVED' AND file_url IS NOT NULL",
                    (doc["em_id"],)
                )
                if cursor.fetchone()["c"] == 0:
                    cursor.execute("SELECT em_name FROM employers WHERE em_id = %s", (doc["em_id"],))
                    em_info = cursor.fetchone()
                    cursor.execute(
                        """
                        INSERT INTO admin_logs
                            (admin_id, action_type, target_type, target_id, target_name, note)
                        VALUES (%s, 'VERIFY_EMPLOYER', 'EMPLOYER', %s, %s, 'All documents approved')
                        """,
                        (body.reviewed_by, doc["em_id"], em_info["em_name"] if em_info else doc["em_id"])
                    )
            elif body.status == "PENDING":
                cursor.execute(
                    """
                    INSERT INTO admin_logs
                        (admin_id, action_type, target_type, target_id, target_name, note)
                    VALUES (%s, 'RESET_DOCUMENT', 'DOCUMENT', %s, %s, %s)
                    """,
                    (body.reviewed_by, doc_id, doc_info["em_name"], doc_label)
                )

        conn.commit()
        return {"status": "updated", "doc_id": doc_id, "new_status": body.status}
    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR] review_em_document: {e}")
        if conn:
            conn.rollback()
        return {"error": str(e)}
    finally:
        if conn:
            conn.close()

@router.patch("/employers/{em_id}/ban")
def ban_employer(em_id: str, body: BanRequest):
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute("SELECT em_id FROM employers WHERE em_id = %s", (em_id,))
        if not cursor.fetchone():
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
            INSERT INTO admin_logs
                (admin_id, action_type, target_type, target_id, target_name, note)
            VALUES (%s, %s, 'EMPLOYER', %s, %s, NULL)
            """,
            (body.admin_id, action, em_id, em_info["em_name"] if em_info else em_id)
        )
        conn.commit()
        return {"status": "updated", "em_id": em_id, "is_active": body.is_active}
    except HTTPException:
        raise
    except Exception as e:
        return {"error": str(e)}
    finally:
        if conn:
            conn.close()