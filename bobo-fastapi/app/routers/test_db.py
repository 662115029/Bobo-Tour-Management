from fastapi import APIRouter
from app.db.connection import get_connection

router = APIRouter()

@router.get("/test-db")
def test_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM admins")
    data = cursor.fetchall()

    conn.close()

    return data