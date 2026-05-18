from fastapi import APIRouter, HTTPException, Header
from typing import Optional
from app.db.connection import get_connection, get_cursor

router = APIRouter(tags=["jobs"])


@router.get("/jobs")
def get_jobs(limit: int = 50, offset: int = 0):
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute(
            """
            SELECT j.job_id, j.em_id, em.em_name AS company,
                   j.job_title, j.job_description,
                   j.job_start_date, j.job_end_date,
                   j.job_required_vehicle_type, j.job_required_seat,
                   j.job_price, j.job_status,
                   j.selected_fl_id, f.fl_name AS selected_driver,
                   j.job_created_at, j.job_updated_at
            FROM jobs j
            JOIN employers em ON j.em_id = em.em_id
            LEFT JOIN freelancers f ON j.selected_fl_id = f.fl_id
            ORDER BY j.job_created_at DESC
            LIMIT %s OFFSET %s
            """,
            (limit, offset),
        )
        rows = cursor.fetchall()
        conn.close()
        return {"items": rows, "limit": limit, "offset": offset}
    except Exception as e:
        return {"error": str(e), "items": []}


@router.post("/jobs")
def create_job(data: dict):
    try:
        conn = get_connection()
        cursor = get_cursor(conn)

        job_id = data.get('job_id')
        em_id = data.get('em_id')
        job_title = data.get('job_title')
        job_description = data.get('job_description')
        job_start_date = data.get('job_start_date')
        job_end_date = data.get('job_end_date')
        job_required_vehicle_type = data.get('job_required_vehicle_type', 'VAN')
        job_required_seat = data.get('job_required_seat', 9)
        job_price = data.get('job_price', 0)
        driver_name = data.get('driver_name')
        driver_phone = data.get('driver_phone')

        cursor.execute("""
            INSERT INTO jobs (job_id, em_id, job_title, job_description, job_start_date, job_end_date,
                           job_required_vehicle_type, job_required_seat, job_price, driver_name, driver_phone)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (job_id, em_id, job_title, job_description, job_start_date, job_end_date,
             job_required_vehicle_type, job_required_seat, job_price, driver_name, driver_phone))

        languages = data.get('job_required_languages', [])
        for lang in languages:
            cursor.execute("INSERT INTO job_required_languages (job_req_lg_id, job_id, language_name) VALUES (%s, %s, %s)",
                          (f"LG{job_id[-6:]}", job_id, lang))

        itineraries = data.get('job_itineraries', [])
        for idx, it in enumerate(itineraries):
            if it.get('place_name'):
                cursor.execute("""
                    INSERT INTO job_itineraries (job_itinerary_id, job_id, place_name, start_time, end_time, note)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (f"IT{job_id[-6:]}{idx}", job_id, it.get('place_name'), it.get('start_time'), it.get('end_time'), it.get('note')))

        pickups = data.get('job_pickups', [])
        for idx, p in enumerate(pickups):
            if p.get('pickup_location'):
                cursor.execute("""
                    INSERT INTO job_pickups (job_pickup_id, job_id, hotel_name, pickup_location, pickup_time, sequence)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (f"PK{job_id[-6:]}{idx}", job_id, p.get('hotel_name'), p.get('pickup_location'), p.get('pickup_time'), idx + 1))

        customers = data.get('job_customers', [])
        for idx, c in enumerate(customers):
            if c.get('customer_name'):
                cursor.execute("""
                    INSERT INTO job_customers (job_customer_id, job_id, customer_name, pax_count, note)
                    VALUES (%s, %s, %s, %s, %s)
                """, (f"CUS{job_id[-6:]}{idx}", job_id, c.get('customer_name'), c.get('pax_count'), c.get('note')))

        inclusions = data.get('job_inclusions', [])
        for idx, inc in enumerate(inclusions):
            if inc.get('description'):
                cursor.execute("""
                    INSERT INTO job_inclusions (job_inclusion_id, job_id, inclusion_type, description, sequence)
                    VALUES (%s, %s, %s, %s, %s)
                """, (f"INC{job_id[-6:]}{idx}", job_id, inc.get('inclusion_type'), inc.get('description'), idx + 1))

        entrance_fees = data.get('job_entrance_fees', [])
        for idx, fee in enumerate(entrance_fees):
            if fee.get('place_name'):
                cursor.execute("""
                    INSERT INTO job_entrance_fees (job_entrance_fee_id, job_id, place_name, thai_price, foreigner_price, sequence)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (f"EF{job_id[-6:]}{idx}", job_id, fee.get('place_name'), fee.get('thai_price'), fee.get('foreigner_price'), idx + 1))

        conn.commit()
        conn.close()
        return {"success": True, "job_id": job_id}
    except Exception as e:
        return {"error": str(e)}


@router.get("/job-required-languages")
def get_job_required_languages(limit: int = 50, offset: int = 0):
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute(
            """
            SELECT jrl.job_req_lg_id, jrl.job_id, j.job_title,
                   jrl.language_name, jrl.created_at
            FROM job_required_languages jrl
            JOIN jobs j ON jrl.job_id = j.job_id
            ORDER BY j.job_title, jrl.language_name
            LIMIT %s OFFSET %s
            """,
            (limit, offset)
        )
        rows = cursor.fetchall()
        conn.close()
        return {"items": rows, "limit": limit, "offset": offset}
    except Exception as e:
        return {"error": str(e), "items": []}


@router.get("/job-itineraries")
def get_job_itineraries(limit: int = 50, offset: int = 0):
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute(
            """
            SELECT ji.job_itinerary_id, ji.job_id, j.job_title,
                   ji.place_name, ji.start_time, ji.end_time,
                   ji.note, ji.sequence, ji.created_at
            FROM job_itineraries ji
            JOIN jobs j ON ji.job_id = j.job_id
            ORDER BY ji.job_id, ji.sequence
            LIMIT %s OFFSET %s
            """,
            (limit, offset)
        )
        rows = cursor.fetchall()
        conn.close()
        return {"items": rows, "limit": limit, "offset": offset}
    except Exception as e:
        return {"error": str(e), "items": []}


@router.get("/job-passengers")
def get_job_passengers(limit: int = 50, offset: int = 0):
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute(
            """
            SELECT jp.job_passenger_id, jp.job_id, j.job_title,
                   jp.first_name, jp.last_name,
                   jp.hotel_name, jp.pickup_time,
                   jp.note, jp.created_at
            FROM job_passengers jp
            JOIN jobs j ON jp.job_id = j.job_id
            ORDER BY jp.job_id, jp.pickup_time
            LIMIT %s OFFSET %s
            """,
            (limit, offset)
        )
        rows = cursor.fetchall()
        conn.close()
        return {"items": rows, "limit": limit, "offset": offset}
    except Exception as e:
        return {"error": str(e), "items": []}


@router.get("/job-expenses")
def get_job_expenses(limit: int = 50, offset: int = 0):
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute(
            """
            SELECT je.job_expense_id, je.job_id, j.job_title,
                   je.item_name, je.amount, je.sequence, je.created_at
            FROM job_expenses je
            JOIN jobs j ON je.job_id = j.job_id
            ORDER BY je.job_id, je.sequence
            LIMIT %s OFFSET %s
            """,
            (limit, offset)
        )
        rows = cursor.fetchall()
        conn.close()
        return {"items": rows, "limit": limit, "offset": offset}
    except Exception as e:
        return {"error": str(e), "items": []}


@router.get("/job-applications")
def get_job_applications(limit: int = 50, offset: int = 0):
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute(
            """
            SELECT ja.job_application_id, ja.job_id, j.job_title,
                   ja.fl_id, f.fl_name AS driver_name,
                   ja.application_status, ja.applied_at, ja.updated_at
            FROM job_applications ja
            JOIN jobs j ON ja.job_id = j.job_id
            JOIN freelancers f ON ja.fl_id = f.fl_id
            ORDER BY ja.applied_at DESC
            LIMIT %s OFFSET %s
            """,
            (limit, offset)
        )
        rows = cursor.fetchall()
        conn.close()
        return {"items": rows, "limit": limit, "offset": offset}
    except Exception as e:
        return {"error": str(e), "items": []}


@router.get("/job-payments")
def get_job_payments(limit: int = 50, offset: int = 0):
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute(
            """
            SELECT jp.payment_id, jp.job_id, j.job_title,
                   jp.em_id, em.em_name AS company,
                   jp.fl_id, f.fl_name AS driver_name,
                   jp.payment_status, jp.slip_url, jp.reject_reason,
                   jp.paid_at, jp.confirmed_at, jp.updated_at
            FROM job_payments jp
            JOIN jobs j ON jp.job_id = j.job_id
            JOIN employers em ON jp.em_id = em.em_id
            JOIN freelancers f ON jp.fl_id = f.fl_id
            ORDER BY jp.paid_at DESC
            LIMIT %s OFFSET %s
            """,
            (limit, offset)
        )
        rows = cursor.fetchall()
        conn.close()
        return {"items": rows, "limit": limit, "offset": offset}
    except Exception as e:
        return {"error": str(e), "items": []}


@router.delete("/jobs/{job_id}")
def delete_job(job_id: str, x_admin_id: Optional[str] = Header(None, alias="X-Admin-ID")):
    admin_id = x_admin_id
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute("SELECT job_id, job_title FROM jobs WHERE job_id = %s", (job_id,))
        job = cursor.fetchone()
        if not job:
            conn.close()
            raise HTTPException(status_code=404, detail="Job not found")

        job_title = job["job_title"] if job else job_id

        cursor.execute("DELETE FROM fl_reviews WHERE job_id = %s", (job_id,))
        cursor.execute("DELETE FROM em_reviews WHERE job_id = %s", (job_id,))
        cursor.execute("DELETE FROM job_payments WHERE job_id = %s", (job_id,))
        cursor.execute("DELETE FROM job_applications WHERE job_id = %s", (job_id,))
        cursor.execute("DELETE FROM job_expenses WHERE job_id = %s", (job_id,))
        cursor.execute("DELETE FROM job_passengers WHERE job_id = %s", (job_id,))
        cursor.execute("DELETE FROM job_itineraries WHERE job_id = %s", (job_id,))
        cursor.execute("DELETE FROM job_required_languages WHERE job_id = %s", (job_id,))
        cursor.execute("DELETE FROM jobs WHERE job_id = %s", (job_id,))

        conn.commit()
        conn.close()

        print(f"DEBUG: admin_id={admin_id}, type={type(admin_id)}, bool(admin_id)={bool(admin_id)}")
        if admin_id:
            try:
                print(f"Inserting log for admin_id={admin_id}, job_id={job_id}")
                log_conn = get_connection()
                log_cursor = get_cursor(log_conn)
                log_cursor.execute(
                    """
                    INSERT INTO admin_logs
                        (admin_id, action_type, target_type, target_id, target_name, note)
                    VALUES (%s, 'DELETE_JOB', 'JOB', %s, %s, NULL)
                    """,
                    (admin_id, job_id, job_title)
                )
                log_conn.commit()
                log_conn.close()
                print(f"Log inserted successfully")
            except Exception as log_error:
                print(f"ERROR inserting log: {str(log_error)}")
                if log_conn:
                    log_conn.close()
        else:
            print(f"Skipping log insert: admin_id is None or empty")

        return {"status": "deleted", "job_id": job_id}
    except HTTPException:
        raise
    except Exception as e:
        if conn:
            conn.rollback()
            conn.close()
        raise HTTPException(status_code=500, detail=f"Failed to delete job: {str(e)}")