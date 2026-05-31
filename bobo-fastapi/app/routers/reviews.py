from fastapi import APIRouter
from typing import Optional
from app.db.connection import get_connection, get_cursor

router = APIRouter(tags=["reviews"])


@router.get("/fl-reviews")
def get_fl_reviews(limit: int = 50, offset: int = 0, fl_id: Optional[int] = None, em_id: Optional[int] = None):
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        where = []
        params = []
        if fl_id:
            where.append("fr.fl_id = %s")
            params.append(fl_id)
        if em_id:
            where.append("fr.em_id = %s")
            params.append(em_id)
        where_sql = ("WHERE " + " AND ".join(where)) if where else ""
        params += [limit, offset]
        cursor.execute(
            f"""
            SELECT fr.fl_review_id, fr.job_id, j.job_title,
                   fr.em_id, em.em_name AS company,
                   fr.fl_id, f.fl_name AS driver_name,
                   fr.rating, fr.comment, fr.reviewed_at
            FROM fl_reviews fr
            JOIN jobs j ON fr.job_id = j.job_id
            JOIN employers em ON fr.em_id = em.em_id
            JOIN freelancers f ON fr.fl_id = f.fl_id
            {where_sql}
            ORDER BY fr.reviewed_at DESC
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

@router.get("/em-reviews")
def get_em_reviews(limit: int = 50, offset: int = 0, em_id: Optional[int] = None, fl_id: Optional[int] = None):
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        where = []
        params = []
        if em_id:
            where.append("er.em_id = %s")
            params.append(em_id)
        if fl_id:
            where.append("er.fl_id = %s")
            params.append(fl_id)
        where_sql = ("WHERE " + " AND ".join(where)) if where else ""
        params += [limit, offset]
        cursor.execute(
            f"""
            SELECT er.em_review_id, er.job_id, j.job_title,
                   er.fl_id, f.fl_name AS driver_name,
                   er.em_id, em.em_name AS company,
                   er.rating, er.comment, er.reviewed_at
            FROM em_reviews er
            JOIN jobs j ON er.job_id = j.job_id
            JOIN freelancers f ON er.fl_id = f.fl_id
            JOIN employers em ON er.em_id = em.em_id
            {where_sql}
            ORDER BY er.reviewed_at DESC
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