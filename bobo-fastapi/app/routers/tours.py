from fastapi import APIRouter, HTTPException
from app.db.connection import get_connection, get_cursor

router = APIRouter(tags=["tours"])


def _upsert_language(cursor, name: str) -> int:
    cursor.execute("INSERT IGNORE INTO languages (language_name) VALUES (%s)", (name,))
    cursor.execute("SELECT language_id FROM languages WHERE language_name = %s", (name,))
    return cursor.fetchone()["language_id"]


def _format_time(val):
    """Convert seconds int or HH:MM string to HH:MM, return None if empty."""
    if val is None or val == '':
        return None
    try:
        secs = int(val)
        h, m = divmod(secs // 60, 60)
        return f"{h:02d}:{m:02d}"
    except (ValueError, TypeError):
        return str(val)[:5] or None


@router.get("/tours")
def get_employer_tours(em_id: str, limit: int = 50, offset: int = 0):
    conn = None
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
            WHERE j.em_id = %s
            ORDER BY j.job_created_at DESC
            LIMIT %s OFFSET %s
            """,
            (em_id, limit, offset),
        )
        return cursor.fetchall()
    except Exception:
        return []
    finally:
        if conn:
            conn.close()


@router.get("/tours/{job_id}")
def get_tour(job_id: str, em_id: str):
    conn = None
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
                   j.selected_fl_id,
                   f.fl_name AS driver_name,
                   f.fl_phone AS driver_phone,
                   f.fl_profile_image_url AS driver_profile_image_url,
                   j.job_created_at, j.job_updated_at
            FROM jobs j
            JOIN employers em ON j.em_id = em.em_id
            LEFT JOIN freelancers f ON j.selected_fl_id = f.fl_id
            WHERE j.job_id = %s AND j.em_id = %s
            """,
            (job_id, em_id)
        )
        job = cursor.fetchone()
        if not job:
            raise HTTPException(status_code=404, detail="Tour not found")

        job = dict(job)

        try:
            cursor.execute(
                """
                SELECT l.language_name
                FROM job_required_languages jrl
                JOIN languages l ON jrl.language_id = l.language_id
                WHERE jrl.job_id = %s
                ORDER BY l.language_name
                """,
                (job_id,)
            )
            job["job_required_languages"] = [r["language_name"] for r in cursor.fetchall()]
        except Exception:
            job["job_required_languages"] = []

        try:
            cursor.execute(
                "SELECT place_name, start_time, end_time, note FROM job_itineraries WHERE job_id = %s ORDER BY sequence, start_time",
                (job_id,)
            )
            job["job_itineraries"] = [dict(r) for r in cursor.fetchall()]
        except Exception:
            job["job_itineraries"] = []

        try:
            cursor.execute(
                """
                SELECT job_passenger_id, first_name, last_name, hotel_name, pickup_time, note
                FROM job_passengers WHERE job_id = %s ORDER BY job_passenger_id
                """,
                (job_id,)
            )
            job["job_passengers"] = [dict(r) for r in cursor.fetchall()]
        except Exception:
            job["job_passengers"] = []

        try:
            # Fixed: return as job_expenses with item_name and amount to match frontend
            cursor.execute(
                "SELECT item_name, amount, sequence FROM job_expenses WHERE job_id = %s ORDER BY sequence",
                (job_id,)
            )
            job["job_expenses"] = [dict(r) for r in cursor.fetchall()]
        except Exception:
            job["job_expenses"] = []

        return job
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()


@router.post("/tours")
def create_tour(data: dict):
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)

        cursor.execute(
            """
            INSERT INTO jobs (em_id, job_title, job_description, job_start_date, job_end_date,
                              job_required_vehicle_type, job_required_seat, job_price)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                data.get("em_id"),
                data.get("job_title"),
                data.get("job_description"),
                data.get("job_start_date"),
                data.get("job_end_date"),
                data.get("job_required_vehicle_type", "VAN"),
                data.get("job_required_seat", 9),
                data.get("job_price") or 0,  # Fixed: treat None as 0
            ),
        )
        job_id = cursor.lastrowid
        job_start_date = data.get("job_start_date")

        for lang_name in data.get("job_required_languages", []):
            if lang_name:
                lang_id = _upsert_language(cursor, lang_name)
                cursor.execute(
                    "INSERT IGNORE INTO job_required_languages (job_id, language_id) VALUES (%s, %s)",
                    (job_id, lang_id),
                )

        for idx, it in enumerate(data.get("job_itineraries", [])):
            if it.get("place_name"):
                cursor.execute(
                    """
                    INSERT INTO job_itineraries (job_id, itinerary_date, place_name, start_time, end_time, note, sequence)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """,
                    (job_id,
                     it.get("itinerary_date") or job_start_date,
                     it.get("place_name"),
                     it.get("start_time") or "00:00",
                     it.get("end_time") or "00:00",
                     it.get("note") or None,
                     idx + 1),
                )

        for idx, p in enumerate(data.get("job_passengers", [])):
            if p.get("first_name"):
                cursor.execute(
                    """
                    INSERT INTO job_passengers (job_id, first_name, last_name, hotel_name, pickup_time, note)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (job_id, p.get("first_name"), p.get("last_name") or None,
                     p.get("hotel_name") or None, _format_time(p.get("pickup_time")),
                     p.get("note") or None),
                )

        # Fixed: read job_expenses (not job_entrance_fees), use item_name and amount
        for idx, exp in enumerate(data.get("job_expenses", [])):
            if exp.get("item_name"):
                cursor.execute(
                    "INSERT INTO job_expenses (job_id, item_name, amount, sequence) VALUES (%s, %s, %s, %s)",
                    (job_id, exp.get("item_name"), exp.get("amount", 0), idx + 1),
                )

        conn.commit()
        return {"success": True, "job_id": job_id}
    except Exception as e:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))  # Fixed: return proper error status
    finally:
        if conn:
            conn.close()


@router.put("/tours/{job_id}")
def update_tour(job_id: str, data: dict):
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)

        em_id = data.get("em_id")
        cursor.execute(
            "SELECT job_id, job_start_date, job_status FROM jobs WHERE job_id = %s AND em_id = %s",
            (job_id, em_id)
        )
        job = cursor.fetchone()
        if not job:
            raise HTTPException(status_code=404, detail="Tour not found")
        if job["job_status"] != "OPEN":
            raise HTTPException(status_code=400, detail="Only OPEN tours can be edited")

        job_start_date = data.get("job_start_date") or job["job_start_date"]

        cursor.execute(
            """
            UPDATE jobs SET
                job_title = %s, job_description = %s,
                job_start_date = %s, job_end_date = %s,
                job_required_vehicle_type = %s, job_required_seat = %s,
                job_price = %s
            WHERE job_id = %s
            """,
            (
                data.get("job_title"), data.get("job_description"),
                data.get("job_start_date"), data.get("job_end_date"),
                data.get("job_required_vehicle_type", "VAN"),
                data.get("job_required_seat", 9),
                data.get("job_price") or 0,  # Fixed: treat None as 0
                job_id,
            ),
        )

        cursor.execute("DELETE FROM job_required_languages WHERE job_id = %s", (job_id,))
        for lang_name in data.get("job_required_languages", []):
            if lang_name:
                lang_id = _upsert_language(cursor, lang_name)
                cursor.execute(
                    "INSERT IGNORE INTO job_required_languages (job_id, language_id) VALUES (%s, %s)",
                    (job_id, lang_id),
                )

        cursor.execute("DELETE FROM job_itineraries WHERE job_id = %s", (job_id,))
        for idx, it in enumerate(data.get("job_itineraries", [])):
            if it.get("place_name"):
                cursor.execute(
                    """
                    INSERT INTO job_itineraries (job_id, itinerary_date, place_name, start_time, end_time, note, sequence)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """,
                    (job_id,
                     it.get("itinerary_date") or job_start_date,
                     it.get("place_name"),
                     it.get("start_time") or "00:00",
                     it.get("end_time") or "00:00",
                     it.get("note") or None,
                     idx + 1),
                )

        cursor.execute("DELETE FROM job_passengers WHERE job_id = %s", (job_id,))
        for idx, p in enumerate(data.get("job_passengers", [])):
            if p.get("first_name"):
                cursor.execute(
                    """
                    INSERT INTO job_passengers (job_id, first_name, last_name, hotel_name, pickup_time, note)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (job_id, p.get("first_name"), p.get("last_name") or None,
                     p.get("hotel_name") or None, _format_time(p.get("pickup_time")),
                     p.get("note") or None),
                )

        # Fixed: read job_expenses (not job_entrance_fees), use item_name and amount
        cursor.execute("DELETE FROM job_expenses WHERE job_id = %s", (job_id,))
        for idx, exp in enumerate(data.get("job_expenses", [])):
            if exp.get("item_name"):
                cursor.execute(
                    "INSERT INTO job_expenses (job_id, item_name, amount, sequence) VALUES (%s, %s, %s, %s)",
                    (job_id, exp.get("item_name"), exp.get("amount", 0), idx + 1),
                )

        conn.commit()
        return {"success": True, "job_id": job_id}
    except HTTPException:
        raise
    except Exception as e:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))  # Fixed: return proper error status
    finally:
        if conn:
            conn.close()


@router.patch("/tours/{job_id}/cancel")
def cancel_tour(job_id: str, em_id: str):
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)

        cursor.execute(
            "SELECT job_status FROM jobs WHERE job_id = %s AND em_id = %s",
            (job_id, em_id)
        )
        job = cursor.fetchone()
        if not job:
            raise HTTPException(status_code=404, detail="Tour not found")

        if job["job_status"] not in ("OPEN", "MATCHING", "MATCHED"):
            raise HTTPException(
                status_code=400,
                detail=f"Cannot cancel a tour with status '{job['job_status']}'.",
            )

        cursor.execute(
            "UPDATE jobs SET job_status = 'CANCELLED' WHERE job_id = %s",
            (job_id,)
        )
        conn.commit()
        return {"status": "cancelled", "job_id": job_id}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()


@router.get("/tours/{job_id}/applications")
def get_tour_applications(job_id: str, em_id: str):
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)

        cursor.execute(
            "SELECT job_id FROM jobs WHERE job_id = %s AND em_id = %s",
            (job_id, em_id)
        )
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Tour not found")

        cursor.execute(
            """
            SELECT
                ja.job_application_id AS application_id,
                ja.job_id,
                ja.fl_id,
                f.fl_name AS guide_name,
                f.fl_phone AS guide_phone,
                ja.application_status AS status,
                ja.applied_at,
                ja.updated_at
            FROM job_applications ja
            JOIN freelancers f ON ja.fl_id = f.fl_id
            WHERE ja.job_id = %s
            ORDER BY ja.applied_at DESC
            """,
            (job_id,)
        )
        applications = [dict(row) for row in cursor.fetchall()]

        for app in applications:
            try:
                cursor.execute(
                    """
                    SELECT l.language_name
                    FROM fl_languages fll
                    JOIN languages l ON fll.language_id = l.language_id
                    WHERE fll.fl_id = %s
                    """,
                    (app["fl_id"],)
                )
                app["languages"] = [r["language_name"] for r in cursor.fetchall()]
            except Exception:
                app["languages"] = []

        return applications
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()