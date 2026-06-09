from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.db.connection import get_connection, get_cursor
import bcrypt

router = APIRouter(prefix="/auth", tags=["auth"])

EM_DOC_TYPES = [
    "COMPANY_REGISTRATION",
    "BUSINESS_LICENSE",
    "TOURISM_LICENSE",
    "TAX_ID_DOCUMENT",
    "AUTHORIZED_PERSON_ID",
]


class LoginRequest(BaseModel):
    identifier: str
    password: str


class RegisterRequest(BaseModel):
    em_username: str
    em_name: str
    password: str
    em_email: Optional[str] = None
    em_phone: Optional[str] = None
    em_address: Optional[str] = None
    em_bio: Optional[str] = None


@router.get("/check-username")
def check_username(username: str):
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute("SELECT em_id FROM employers WHERE em_username = %s", (username,))
        taken = cursor.fetchone() is not None
        return {"taken": taken}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()


@router.post("/login")
def employer_login(body: LoginRequest):
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute(
            "SELECT em_id, em_username, em_name, em_email, em_password_hash, em_profile_image_url FROM employers WHERE em_username = %s OR em_email = %s",
            (body.identifier, body.identifier)
        )
        employer = cursor.fetchone()
        if not employer:
            raise HTTPException(status_code=401, detail="Invalid username or password.")
        if not bcrypt.checkpw(body.password.encode(), employer["em_password_hash"].encode()):
            raise HTTPException(status_code=401, detail="Invalid username or password.")
        return {
            "em_id": employer["em_id"],
            "em_username": employer["em_username"],
            "em_name": employer["em_name"],
            "em_email": employer["em_email"],
            "em_profile_image_url": employer["em_profile_image_url"],
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()


@router.post("/register", status_code=201)
def employer_register(body: RegisterRequest):
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)

        cursor.execute(
            "SELECT em_id FROM employers WHERE em_username = %s",
            (body.em_username,)
        )
        if cursor.fetchone():
            raise HTTPException(status_code=409, detail="Username already taken.")

        if body.em_email:
            cursor.execute(
                "SELECT em_id FROM employers WHERE em_email = %s",
                (body.em_email,)
            )
            if cursor.fetchone():
                raise HTTPException(status_code=409, detail="Email already taken.")

        password_hash = bcrypt.hashpw(body.password.encode(), bcrypt.gensalt()).decode()

        cursor.execute(
            """
            INSERT INTO employers (em_username, em_email, em_password_hash, em_name, em_phone, em_address, em_bio)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (body.em_username, body.em_email, password_hash,
             body.em_name, body.em_phone, body.em_address, body.em_bio)
        )
        em_id = cursor.lastrowid

        for doc_type in EM_DOC_TYPES:
            cursor.execute(
                "INSERT INTO em_documents (em_id, em_doc_type) VALUES (%s, %s)",
                (em_id, doc_type)
            )

        cursor.execute(
            "INSERT INTO em_verification (em_id, em_verify_status) VALUES (%s, 'PENDING')",
            (em_id,)
        )

        conn.commit()
        return {"message": "Account created successfully.", "em_id": em_id}
    except HTTPException:
        raise
    except Exception as e:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()

class FreelancerLoginRequest(BaseModel):
    identifier: str
    pin: str


@router.post("/freelancer-login")
def freelancer_login(body: FreelancerLoginRequest):
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute(
            """
            SELECT fl_id, fl_username, fl_name, fl_email, fl_phone,
                   fl_pin_hash, fl_profile_image_url, fl_verify_status, fl_is_active
            FROM freelancers
            WHERE fl_username = %s OR fl_email = %s
            """,
            (body.identifier, body.identifier)
        )
        fl = cursor.fetchone()
        if not fl:
            raise HTTPException(status_code=401, detail="Invalid username or PIN.")
        if not fl["fl_is_active"]:
            raise HTTPException(status_code=403, detail="Account is disabled.")
        if not bcrypt.checkpw(body.pin.encode(), fl["fl_pin_hash"].encode()):
            raise HTTPException(status_code=401, detail="Invalid username or PIN.")
        return {
            "fl_id": fl["fl_id"],
            "fl_username": fl["fl_username"],
            "fl_name": fl["fl_name"],
            "fl_email": fl["fl_email"],
            "fl_phone": fl["fl_phone"],
            "fl_profile_image_url": fl["fl_profile_image_url"],
            "fl_verify_status": fl["fl_verify_status"],
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()


@router.get("/gen-hash")
def gen_hash(pin: str):
    return {"hash": bcrypt.hashpw(pin.encode(), bcrypt.gensalt()).decode()}