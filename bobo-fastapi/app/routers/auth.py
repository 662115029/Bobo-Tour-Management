from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.db.connection import get_connection, get_cursor
import bcrypt
import uuid

router = APIRouter(prefix="/auth", tags=["auth"])


class LoginRequest(BaseModel):
    em_username: str
    password: str


class RegisterRequest(BaseModel):
    em_username: str
    em_name: str
    password: str
    em_phone: Optional[str] = None
    em_address: Optional[str] = None
    em_bio: Optional[str] = None


@router.post("/login")
def employer_login(body: LoginRequest):
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute(
            "SELECT em_id, em_username, em_name, em_password_hash FROM employers WHERE em_username = %s",
            (body.em_username,)
        )
        employer = cursor.fetchone()
        conn.close()

        if not employer:
            raise HTTPException(status_code=401, detail="Invalid username or password.")

        if not bcrypt.checkpw(body.password.encode(), employer["em_password_hash"].encode()):
            raise HTTPException(status_code=401, detail="Invalid username or password.")

        return {
            "em_id": employer["em_id"],
            "em_username": employer["em_username"],
            "em_name": employer["em_name"],
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/register", status_code=201)
def employer_register(body: RegisterRequest):
    try:
        conn = get_connection()
        cursor = get_cursor(conn)

        cursor.execute(
            "SELECT em_id FROM employers WHERE em_username = %s",
            (body.em_username,)
        )
        if cursor.fetchone():
            conn.close()
            raise HTTPException(status_code=409, detail="Username already taken.")

        em_id = str(uuid.uuid4())
        password_hash = bcrypt.hashpw(body.password.encode(), bcrypt.gensalt()).decode()

        cursor.execute(
            """
            INSERT INTO employers (em_id, em_username, em_password_hash, em_name, em_phone, em_address, em_bio)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (em_id, body.em_username, password_hash, body.em_name,
             body.em_phone, body.em_address, body.em_bio)
        )
        conn.commit()
        conn.close()
        return {"message": "Account created successfully."}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
