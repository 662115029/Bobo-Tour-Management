from fastapi import APIRouter, HTTPException
from typing import Optional
from app.db.connection import get_connection, get_cursor
from notification import notify_job_confirmed, notify_job_declined

router = APIRouter(tags=["jobs"])


class JobResponseRequest:
    def __init__(self, line_user_id: str, job_id: str):
        self.line_user_id = line_user_id
        self.job_id = job_id


@router.get("/jobs")
def get_jobs(limit: int = 50, offset: int = 0, em_id: Optional[str] = None):
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        if em_id:
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
                WHERE j.em_id = %s
                ORDER BY j.job_created_at DESC
                LIMIT %s OFFSET %s
                """,
                (em_id, limit, offset),
            )
        else:
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
        return rows
    except Exception as e:
        return []


# ── NEW: Get single job with all nested data ───────────────────────────────
@router.get("/jobs/{job_id}")
def get_job(job_id: str):
    try:
        conn = get_connection()
        cursor = get_cursor(conn)

        # Check which columns actually exist in the jobs table so optional/
        # not-yet-migrated columns never cause a crash.
        cursor.execute("SHOW COLUMNS FROM jobs")
        existing_columns = {row["Field"] for row in cursor.fetchall()}

        # Full wishlist — only columns that exist will be selected
        desired_columns = [
            "job_id", "em_id", "job_title", "job_description",
            "job_start_date", "job_end_date",
            "job_required_vehicle_type", "job_required_seat",
            "job_price", "job_status",
            "selected_fl_id", "job_created_at", "job_updated_at",
        ]
        select_parts = [f"j.{col}" for col in desired_columns if col in existing_columns]
        select_clause = ", ".join(select_parts)

        cursor.execute(
            f"""
            SELECT {select_clause},
                   em.em_name AS company,
                   f.fl_name AS selected_driver
            FROM jobs j
            JOIN employers em ON j.em_id = em.em_id
            LEFT JOIN freelancers f ON j.selected_fl_id = f.fl_id
            WHERE j.job_id = %s
            """,
            (job_id,)
        )
        job = cursor.fetchone()
        if not job:
            conn.close()
            raise HTTPException(status_code=404, detail="Job not found")

        job = dict(job)

        # Languages
        try:
            cursor.execute(
                "SELECT language_name FROM job_required_languages WHERE job_id = %s ORDER BY language_name",
                (job_id,)
            )
            job["job_required_languages"] = [r["language_name"] for r in cursor.fetchall()]
        except Exception:
            job["job_required_languages"] = []

        # Itineraries
        try:
            cursor.execute(
                "SELECT place_name, start_time, end_time, note FROM job_itineraries WHERE job_id = %s ORDER BY start_time",
                (job_id,)
            )
            job["job_itineraries"] = [dict(r) for r in cursor.fetchall()]
        except Exception:
            job["job_itineraries"] = []

        # Pickup points (job_passengers with no last_name)
        try:
            cursor.execute(
                "SELECT first_name AS pickup_location, hotel_name, pickup_time FROM job_passengers WHERE job_id = %s AND last_name IS NULL ORDER BY job_passenger_id",
                (job_id,)
            )
            job["job_pickups"] = [dict(r) for r in cursor.fetchall()]
        except Exception:
            job["job_pickups"] = []

        # Customers (job_passengers with last_name or note)
        try:
            cursor.execute(
                "SELECT CONCAT(first_name, IFNULL(CONCAT(' ', last_name), '')) AS customer_name, note FROM job_passengers WHERE job_id = %s AND last_name IS NOT NULL ORDER BY job_passenger_id",
                (job_id,)
            )
            job["job_customers"] = [dict(r) for r in cursor.fetchall()]
        except Exception:
            job["job_customers"] = []

        # Inclusions & exclusions
        try:
            cursor.execute(
                "SELECT inclusion_type, description, sequence FROM job_inclusions WHERE job_id = %s ORDER BY sequence",
                (job_id,)
            )
            job["job_inclusions"] = [dict(r) for r in cursor.fetchall()]
        except Exception:
            job["job_inclusions"] = []

        # Entrance fees (job_expenses)
        try:
            cursor.execute(
                "SELECT item_name AS place_name, amount AS foreigner_price, 0 AS thai_price, sequence FROM job_expenses WHERE job_id = %s ORDER BY sequence",
                (job_id,)
            )
            job["job_entrance_fees"] = [dict(r) for r in cursor.fetchall()]
        except Exception:
            job["job_entrance_fees"] = []

        conn.close()
        return job

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── NEW: Cancel a job ──────────────────────────────────────────────────────
@router.patch("/jobs/{job_id}/cancel")
def cancel_job(job_id: str):
    try:
        conn = get_connection()
        cursor = get_cursor(conn)

        cursor.execute("SELECT job_status FROM jobs WHERE job_id = %s", (job_id,))
        job = cursor.fetchone()
        if not job:
            conn.close()
            raise HTTPException(status_code=404, detail="Job not found")

        if job["job_status"] not in ("OPEN", "MATCHING"):
            conn.close()
            raise HTTPException(
                status_code=400,
                detail=f"Cannot cancel a job with status '{job['job_status']}'. Only OPEN or MATCHING jobs can be cancelled."
            )

        cursor.execute(
            "UPDATE jobs SET job_status = 'CANCELLED', job_updated_at = NOW() WHERE job_id = %s",
            (job_id,)
        )
        conn.commit()
        conn.close()
        return {"status": "cancelled", "job_id": job_id}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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
                           job_required_vehicle_type, job_required_seat, job_price)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (job_id, em_id, job_title, job_description, job_start_date, job_end_date,
              job_required_vehicle_type, job_required_seat, job_price))

        languages = data.get('job_required_languages', [])
        for idx, lang in enumerate(languages):
            cursor.execute(
                "INSERT INTO job_required_languages (job_req_lg_id, job_id, language_name) VALUES (%s, %s, %s)",
                (f"LG{job_id[-6:]}{idx}", job_id, lang)
            )

        itineraries = data.get('job_itineraries', [])
        for idx, it in enumerate(itineraries):
            if it.get('place_name'):
                cursor.execute("""
                    INSERT INTO job_itineraries (job_itinerary_id, job_id, place_name, start_time, end_time, note)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (f"IT{job_id[-6:]}{idx}", job_id, it.get('place_name'), it.get('start_time'), it.get('end_time'), it.get('note')))

        # Pickups → job_passengers (no last_name = pickup row)
        for idx, p in enumerate(data.get('job_pickups', [])):
            if p.get('hotel_name') or p.get('pickup_location'):
                cursor.execute("""
                    INSERT INTO job_passengers (job_id, first_name, hotel_name, pickup_time, note)
                    VALUES (%s, %s, %s, %s, %s)
                """, (job_id, p.get('pickup_location'), p.get('hotel_name'), p.get('pickup_time'), None))

        # Customers → job_passengers (has first_name + last_name)
        for idx, c in enumerate(data.get('job_customers', [])):
            if c.get('customer_name'):
                name_parts = (c.get('customer_name') or '').split(' ', 1)
                first = name_parts[0]
                last = name_parts[1] if len(name_parts) > 1 else None
                cursor.execute("""
                    INSERT INTO job_passengers (job_id, first_name, last_name, note)
                    VALUES (%s, %s, %s, %s)
                """, (job_id, first, last, c.get('note')))

        # Inclusions
        for idx, inc in enumerate(data.get('job_inclusions', [])):
            if inc.get('description'):
                cursor.execute("""
                    INSERT INTO job_inclusions (job_inclusion_id, job_id, inclusion_type, description, sequence)
                    VALUES (%s, %s, %s, %s, %s)
                """, (f"INC{job_id[-6:]}{idx}", job_id, inc.get('inclusion_type'), inc.get('description'), idx + 1))

        # Entrance fees → job_expenses
        for idx, fee in enumerate(data.get('job_entrance_fees', [])):
            if fee.get('place_name'):
                cursor.execute("""
                    INSERT INTO job_expenses (job_id, item_name, amount, sequence)
                    VALUES (%s, %s, %s, %s)
                """, (job_id, fee.get('place_name'), fee.get('foreigner_price', 0), idx + 1))

        conn.commit()
        conn.close()
        return {"success": True, "job_id": job_id}
    except Exception as e:
        return {"error": str(e)}


@router.put("/jobs/{job_id}")
def update_job(job_id: str, data: dict):
    try:
        conn = get_connection()
        cursor = get_cursor(conn)

        cursor.execute("SELECT job_id FROM jobs WHERE job_id = %s", (job_id,))
        if not cursor.fetchone():
            conn.close()
            raise HTTPException(status_code=404, detail="Job not found")

        # Update main job row
        cursor.execute("""
            UPDATE jobs SET
                job_title = %s,
                job_description = %s,
                job_start_date = %s,
                job_end_date = %s,
                job_required_vehicle_type = %s,
                job_required_seat = %s,
                job_price = %s,
                job_updated_at = NOW()
            WHERE job_id = %s
        """, (
            data.get('job_title'),
            data.get('job_description'),
            data.get('job_start_date'),
            data.get('job_end_date'),
            data.get('job_required_vehicle_type', 'VAN'),
            data.get('job_required_seat', 9),
            data.get('job_price', 0),
            job_id,
        ))

        # Replace languages
        cursor.execute("DELETE FROM job_required_languages WHERE job_id = %s", (job_id,))
        for idx, lang in enumerate(data.get('job_required_languages', [])):
            cursor.execute(
                "INSERT INTO job_required_languages (job_req_lg_id, job_id, language_name) VALUES (%s, %s, %s)",
                (f"LG{job_id[-6:]}{idx}", job_id, lang)
            )

        # Replace itineraries
        cursor.execute("DELETE FROM job_itineraries WHERE job_id = %s", (job_id,))
        for idx, it in enumerate(data.get('job_itineraries', [])):
            if it.get('place_name'):
                cursor.execute("""
                    INSERT INTO job_itineraries (job_itinerary_id, job_id, place_name, start_time, end_time, note)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (f"IT{job_id[-6:]}{idx}", job_id, it.get('place_name'), it.get('start_time'), it.get('end_time'), it.get('note')))

        # Replace pickups + customers → job_passengers
        cursor.execute("DELETE FROM job_passengers WHERE job_id = %s", (job_id,))
        for idx, p in enumerate(data.get('job_pickups', [])):
            if p.get('hotel_name') or p.get('pickup_location'):
                cursor.execute("""
                    INSERT INTO job_passengers (job_id, first_name, hotel_name, pickup_time, note)
                    VALUES (%s, %s, %s, %s, %s)
                """, (job_id, p.get('pickup_location'), p.get('hotel_name'), p.get('pickup_time'), None))
        for idx, c in enumerate(data.get('job_customers', [])):
            if c.get('customer_name'):
                name_parts = (c.get('customer_name') or '').split(' ', 1)
                first = name_parts[0]
                last = name_parts[1] if len(name_parts) > 1 else None
                cursor.execute("""
                    INSERT INTO job_passengers (job_id, first_name, last_name, note)
                    VALUES (%s, %s, %s, %s)
                """, (job_id, first, last, c.get('note')))

        # Replace inclusions
        cursor.execute("DELETE FROM job_inclusions WHERE job_id = %s", (job_id,))
        for idx, inc in enumerate(data.get('job_inclusions', [])):
            if inc.get('description'):
                cursor.execute("""
                    INSERT INTO job_inclusions (job_inclusion_id, job_id, inclusion_type, description, sequence)
                    VALUES (%s, %s, %s, %s, %s)
                """, (f"INC{job_id[-6:]}{idx}", job_id, inc.get('inclusion_type'), inc.get('description'), idx + 1))

        # Replace entrance fees → job_expenses
        cursor.execute("DELETE FROM job_expenses WHERE job_id = %s", (job_id,))
        for idx, fee in enumerate(data.get('job_entrance_fees', [])):
            if fee.get('place_name'):
                cursor.execute("""
                    INSERT INTO job_expenses (job_id, item_name, amount, sequence)
                    VALUES (%s, %s, %s, %s)
                """, (job_id, fee.get('place_name'), fee.get('foreigner_price', 0), idx + 1))

        conn.commit()
        conn.close()
        return {"success": True, "job_id": job_id}
    except HTTPException:
        raise
    except Exception as e:
        return {"error": str(e)}


@router.delete("/jobs/{job_id}")
def delete_job(job_id: str, admin_id: str = None):
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

        if admin_id:
            cursor.execute(
                """
                INSERT INTO admin_logs (admin_id, action_type, target_type, target_id, target_name, note)
                VALUES (%s, 'DELETE', 'JOB', %s, %s, NULL)
                """,
                (admin_id, job_id, job_title)
            )

        conn.commit()
        conn.close()
        return {"status": "deleted", "job_id": job_id}
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        conn.close()
        return {"error": str(e)}


@router.post("/jobs/{job_id}/accept")
def accept_job(job_id: str, request: dict):
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute(
            """
            SELECT j.job_id, j.job_title, em.em_name, j.job_start_date, j.job_price
            FROM jobs j JOIN employers em ON j.em_id = em.em_id
            WHERE j.job_id = %s
            """,
            (job_id,)
        )
        job = cursor.fetchone()
        if job:
            notify_job_confirmed(request.get("line_user_id"), job)
        conn.close()
        return {"status": "accepted", "job": job if job else None}
    except Exception as e:
        return {"error": str(e)}


@router.post("/jobs/{job_id}/decline")
def decline_job(job_id: str, request: dict):
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute(
            """
            SELECT j.job_id, j.job_title, em.em_name, j.job_start_date, j.job_price
            FROM jobs j JOIN employers em ON j.em_id = em.em_id
            WHERE j.job_id = %s
            """,
            (job_id,)
        )
        job = cursor.fetchone()
        if job:
            notify_job_declined(request.get("line_user_id"), job)
        conn.close()
        return {"status": "declined", "job": job if job else None}
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


@router.get("/job-pickups")
def get_job_pickups(limit: int = 50, offset: int = 0):
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute("SELECT * FROM job_passengers WHERE last_name IS NULL ORDER BY job_id LIMIT %s OFFSET %s", (limit, offset))
        rows = cursor.fetchall()
        conn.close()
        return {"items": rows, "limit": limit, "offset": offset}
    except Exception as e:
        return {"error": str(e), "items": []}


@router.get("/job-customers")
def get_job_customers(limit: int = 50, offset: int = 0):
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute("SELECT * FROM job_passengers WHERE last_name IS NOT NULL LIMIT %s OFFSET %s", (limit, offset))
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
        cursor.execute("SELECT * FROM job_itineraries LIMIT %s OFFSET %s", (limit, offset))
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
        cursor.execute("SELECT * FROM job_applications ORDER BY applied_at DESC LIMIT %s OFFSET %s", (limit, offset))
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
        cursor.execute("SELECT * FROM job_payments LIMIT %s OFFSET %s", (limit, offset))
        rows = cursor.fetchall()
        conn.close()
        return {"items": rows, "limit": limit, "offset": offset}
    except Exception as e:
        return {"error": str(e), "items": []}
