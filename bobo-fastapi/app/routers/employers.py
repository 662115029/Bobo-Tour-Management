from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.db.connection import get_connection, get_cursor

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


class BanRequest(BaseModel):
    is_active: bool
    admin_id: str


@router.post("/employers/register")
def register_employer(body: EmployerRegisterRequest):
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)

        cursor.execute(
            "SELECT em_id FROM employers WHERE em_email = %s OR em_username = %s",
            (body.em_email, body.em_username)
        )
        if cursor.fetchone():
            conn.close()
            raise HTTPException(status_code=409, detail="Email or username already taken.")

        cursor.execute(
            """
            INSERT INTO employers
                (em_username, em_email, em_name, em_phone,
                 em_verify_status, em_is_active)
            VALUES (%s, %s, %s, %s, 'PENDING', 1)
            """,
            (body.em_username, body.em_email, body.em_name, body.em_phone)
        )
        em_id = cursor.lastrowid

        cursor.execute(
            """
            INSERT INTO em_verification
                (em_id, em_verify_status, is_latest)
            VALUES (%s, 'PENDING', 1)
            """,
            (em_id,)
        )

        for doc_type in EM_DOC_TYPES:
            cursor.execute(
                """
                INSERT INTO em_documents
                    (em_id, em_doc_type, file_url, em_doc_status)
                VALUES (%s, %s, NULL, 'PENDING')
                """,
                (em_id, doc_type)
            )

        conn.commit()
        conn.close()
        return {"success": True, "em_id": em_id}

    except HTTPException:
        raise
    except Exception as e:
        if conn:
            conn.rollback()
            conn.close()
        return {"success": False, "error": str(e)}


@router.get("/employers")
@router.get("/admin/employers")
def get_employers(limit: int = 10, offset: int = 0, search: str = "", status: str = "", sort_by: str = "em_updated_at", sort_order: str = "desc"):
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
        allowed_sort = {"em_name","em_rating_avg","em_updated_at","em_created_at"}
        safe_sort_by = sort_by if sort_by in allowed_sort else "em_updated_at"
        safe_order = "ASC" if sort_order.lower() == "asc" else "DESC"
        cursor.execute(
            f"""
            SELECT em_id, em_username, em_email, em_name, em_phone, em_address, em_bio,
                   em_profile_image_url, em_verify_status, em_is_active,
                   em_rating_avg, em_created_at, em_updated_at
            FROM employers
            {where_sql}
            ORDER BY {safe_sort_by} {safe_order}
            LIMIT %s OFFSET %s
            """,
            params
        )
        rows = cursor.fetchall()
        conn.close()
        return {"items": rows, "limit": limit, "offset": offset, "search": search, "status": status}
    except Exception as e:
        return {"error": str(e), "items": []}


@router.get("/employers/{em_id}")
def get_employer(em_id: str):
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute(
            """
            SELECT em_id, em_username, em_email, em_name, em_phone, em_address, em_bio,
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


@router.get("/em-bank-accounts")
def get_em_bank_accounts(limit: int = 10, offset: int = 0):
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute(
            """
            SELECT eb.em_bank_account_id, eb.em_id, e.em_name,
                   eb.account_name, eb.account_number, eb.bank_name,
                   eb.is_primary, eb.created_at, eb.updated_at
            FROM em_bank_accounts eb
            JOIN employers e ON eb.em_id = e.em_id
            ORDER BY eb.created_at DESC
            LIMIT %s OFFSET %s
            """,
            (limit, offset)
        )
        rows = cursor.fetchall()
        conn.close()
        return {"items": rows, "limit": limit, "offset": offset}
    except Exception as e:
        return {"error": str(e), "items": []}


@router.get("/em-documents")
def get_em_documents(limit: int = 10, offset: int = 0, status: str = "", em_ids: str = ""):
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        where = []
        params = []
        if em_ids:
            id_list = [int(i) for i in em_ids.split(',') if i.strip().isdigit()]
            placeholders = ','.join(['%s'] * len(id_list))
            where.append(f"ed.em_id IN ({placeholders})")
            params += id_list
        if status:
            where.append("ed.em_doc_status = %s")
            params.append(status)
        elif not em_ids:
            where.append("ed.file_url IS NOT NULL")
        where_sql = "WHERE " + " AND ".join(where) if where else ""
        params += [limit, offset]
        cursor.execute(
            f"""
            SELECT ed.em_doc_id, ed.em_id, e.em_name,
                   ed.em_doc_type, ed.file_url, ed.em_doc_status,
                   ed.em_uploaded_at,
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
        conn.close()
        return {"items": rows, "limit": limit, "offset": offset}
    except Exception as e:
        return {"error": str(e), "items": []}


@router.get("/em-verification")
def get_em_verification(limit: int = 10, offset: int = 0, status: str = "PENDING"):
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        where_sql = "WHERE ev.em_verify_status = %s" if status else ""
        params = ([status] if status else []) + [limit, offset]
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
            ORDER BY ev.em_submitted_at ASC
            LIMIT %s OFFSET %s
            """,
            params
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
                """
                SELECT COUNT(*) AS c FROM em_documents
                WHERE em_id = %s AND em_doc_status != 'APPROVED'
                """,
                (doc["em_id"],)
            )
            if cursor.fetchone()["c"] == 0:
                cursor.execute(
                    "UPDATE employers SET em_verify_status = 'VERIFIED' WHERE em_id = %s",
                    (doc["em_id"],)
                )
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
                "UPDATE employers SET em_verify_status = 'NOT_VERIFIED' WHERE em_id = %s",
                (doc["em_id"],)
            )
            cursor.execute(
                """
                UPDATE em_verification SET em_verify_status = 'NOT_VERIFIED'
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
            action = 'APPROVE_DOCUMENT' if body.status == 'APPROVED' else 'REJECT_DOCUMENT'
            cursor.execute(
                """
                INSERT INTO admin_logs
                    (admin_id, action_type, target_type, target_id, target_name, note)
                VALUES (%s, %s, 'DOCUMENT', %s, %s, %s)
                """,
                (body.reviewed_by, action, doc_id,
                 doc_info["em_name"], doc_info["em_doc_type"])
            )
            if body.status == "APPROVED":
                cursor.execute(
                    "SELECT COUNT(*) AS c FROM em_documents WHERE em_id = %s AND em_doc_status != 'APPROVED'",
                    (doc["em_id"],)
                )
                if cursor.fetchone()["c"] == 0:
                    cursor.execute("SELECT em_name FROM employers WHERE em_id = %s", (doc["em_id"],))
                    em_info = cursor.fetchone()
                    cursor.execute(
                        """
                        INSERT INTO admin_logs
                            (admin_id, action_type, target_type, target_id, target_name, note)
                        VALUES (%s, 'VERIFY_EMPLOYER', 'EMPLOYER', %s, %s, 'All 5 documents approved')
                        """,
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
            INSERT INTO admin_logs
                (admin_id, action_type, target_type, target_id, target_name, note)
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