from fastapi import APIRouter, HTTPException
from app.db.connection import get_connection, get_cursor

router = APIRouter(tags=["tours"])


def _upsert_language(cursor, name: str) -> int:
    cursor.execute("INSERT IGNORE INTO languages (language_name) VALUES (%s)", (name,))
    cursor.execute("SELECT language_id FROM languages WHERE language_name = %s", (name,))
    return cursor.fetchone()["language_id"]


# ── GET /tours ────────────────────────────────────────────────────────────────
# Returns all jobs for an employer.
# job_status values from schema: OPEN, PENDING, MATCHED, IN_PROGRESS, COMPLETED, CANCELLED
@router.get("/tours")
def get_employer_tours(em_id: int, limit: int = 50, offset: int = 0):
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


# ── GET /tours/{job_id} ───────────────────────────────────────────────────────
@router.get("/tours/{job_id}")
def get_tour(job_id: int, em_id: int):
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
            WHERE j.job_id = %s AND j.em_id = %s
            """,
            (job_id, em_id)
        )
        job = cursor.fetchone()
        if not job:
            raise HTTPException(status_code=404, detail="Tour not found")

        job = dict(job)

        # job_required_languages — via junction table
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

        # job_itineraries — columns: place_name, start_time, end_time, note, sequence
        try:
            cursor.execute(
                "SELECT place_name, start_time, end_time, note FROM job_itineraries WHERE job_id = %s ORDER BY sequence, start_time",
                (job_id,)
            )
            job["job_itineraries"] = [dict(r) for r in cursor.fetchall()]
        except Exception:
            job["job_itineraries"] = []

        # job_passengers — split into pickups (no last_name) and customers (has last_name)
        # schema columns: first_name, last_name, hotel_name, pickup_time, note
        try:
            cursor.execute(
                "SELECT first_name AS pickup_location, hotel_name, pickup_time FROM job_passengers WHERE job_id = %s AND last_name IS NULL ORDER BY job_passenger_id",
                (job_id,)
            )
            job["job_pickups"] = [dict(r) for r in cursor.fetchall()]
        except Exception:
            job["job_pickups"] = []

        try:
            cursor.execute(
                "SELECT CONCAT(first_name, IFNULL(CONCAT(' ', last_name), '')) AS customer_name, note FROM job_passengers WHERE job_id = %s AND last_name IS NOT NULL ORDER BY job_passenger_id",
                (job_id,)
            )
            job["job_customers"] = [dict(r) for r in cursor.fetchall()]
        except Exception:
            job["job_customers"] = []

        # job_expenses — schema columns: item_name, amount, sequence
        # NOTE: job_inclusions does NOT exist in the schema — removed entirely
        try:
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


# ── POST /tours ───────────────────────────────────────────────────────────────
@router.post("/tours")
def create_tour(data: dict):
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)

        # jobs table columns: em_id, job_title, job_description, job_start_date,
        #   job_end_date, job_required_vehicle_type, job_required_seat, job_price
        cursor.execute(
            """
            INSERT INTO jobs (em_id, job_title, job_description, job_start_date, job_end_date,
                              job_required_vehicle_type, job_required_seat, job_price)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                int(data.get("em_id")),
                data.get("job_title"),
                data.get("job_description"),
                data.get("job_start_date"),
                data.get("job_end_date"),
                data.get("job_required_vehicle_type", "VAN"),
                data.get("job_required_seat", 9),
                data.get("job_price", 0),
            ),
        )
        job_id = cursor.lastrowid
        job_start_date = data.get("job_start_date")

        # job_required_languages via languages lookup + junction table
        for lang_name in data.get("job_required_languages", []):
            if lang_name:
                lang_id = _upsert_language(cursor, lang_name)
                cursor.execute(
                    "INSERT IGNORE INTO job_required_languages (job_id, language_id) VALUES (%s, %s)",
                    (job_id, lang_id),
                )

        # job_itineraries — itinerary_date required by schema; use job_start_date
        for idx, it in enumerate(data.get("job_itineraries", [])):
            if it.get("place_name"):
                cursor.execute(
                    """
                    INSERT INTO job_itineraries (job_id, itinerary_date, place_name, start_time, end_time, note, sequence)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """,
                    (job_id, job_start_date, it.get("place_name"),
                     it.get("start_time", "00:00"), it.get("end_time", "00:00"),
                     it.get("note"), idx + 1),
                )

        # job_passengers — pickups: no last_name; customers: has last_name
        for p in data.get("job_pickups", []):
            if p.get("hotel_name") or p.get("pickup_location"):
                cursor.execute(
                    "INSERT INTO job_passengers (job_id, first_name, hotel_name, pickup_time) VALUES (%s, %s, %s, %s)",
                    (job_id, p.get("pickup_location", ""), p.get("hotel_name"), p.get("pickup_time")),
                )

        for c in data.get("job_customers", []):
            if c.get("customer_name"):
                parts = (c.get("customer_name") or "").split(" ", 1)
                cursor.execute(
                    "INSERT INTO job_passengers (job_id, first_name, last_name, note) VALUES (%s, %s, %s, %s)",
                    (job_id, parts[0], parts[1] if len(parts) > 1 else None, c.get("note")),
                )

        # job_expenses — schema columns: item_name, amount, sequence
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
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()


# ── PUT /tours/{job_id} ───────────────────────────────────────────────────────
@router.put("/tours/{job_id}")
def update_tour(job_id: int, data: dict):
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)

        em_id = int(data.get("em_id"))
        cursor.execute(
            "SELECT job_id, job_start_date FROM jobs WHERE job_id = %s AND em_id = %s",
            (job_id, em_id)
        )
        job = cursor.fetchone()
        if not job:
            raise HTTPException(status_code=404, detail="Tour not found")

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
                data.get("job_price", 0),
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
                    (job_id, job_start_date, it.get("place_name"),
                     it.get("start_time", "00:00"), it.get("end_time", "00:00"),
                     it.get("note"), idx + 1),
                )

        cursor.execute("DELETE FROM job_passengers WHERE job_id = %s", (job_id,))
        for p in data.get("job_pickups", []):
            if p.get("hotel_name") or p.get("pickup_location"):
                cursor.execute(
                    "INSERT INTO job_passengers (job_id, first_name, hotel_name, pickup_time) VALUES (%s, %s, %s, %s)",
                    (job_id, p.get("pickup_location", ""), p.get("hotel_name"), p.get("pickup_time")),
                )
        for c in data.get("job_customers", []):
            if c.get("customer_name"):
                parts = (c.get("customer_name") or "").split(" ", 1)
                cursor.execute(
                    "INSERT INTO job_passengers (job_id, first_name, last_name, note) VALUES (%s, %s, %s, %s)",
                    (job_id, parts[0], parts[1] if len(parts) > 1 else None, c.get("note")),
                )

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
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()


# ── PATCH /tours/{job_id}/cancel ─────────────────────────────────────────────
# Valid cancellable statuses from schema: OPEN, PENDING, MATCHED
@router.patch("/tours/{job_id}/cancel")
def cancel_tour(job_id: int, em_id: int):
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

        if job["job_status"] not in ("OPEN", "PENDING", "MATCHED"):
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


# ── GET /tours/{job_id}/applications ─────────────────────────────────────────
# application_status values from schema: APPLIED, PENDING, ACCEPTED, REJECTED
@router.get("/tours/{job_id}/applications")
def get_tour_applications(job_id: int, em_id: int):
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


# ── PUT /applications/{application_id}/accept ─────────────────────────────────
# Sets application_status = ACCEPTED (schema: APPLIED, PENDING, ACCEPTED, REJECTED)
@router.put("/applications/{application_id}/accept")
def accept_application(application_id: int):
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)

        cursor.execute(
            "SELECT job_application_id, job_id FROM job_applications WHERE job_application_id = %s",
            (application_id,)
        )
        app = cursor.fetchone()
        if not app:
            raise HTTPException(status_code=404, detail="Application not found")

        cursor.execute(
            "UPDATE job_applications SET application_status = 'ACCEPTED' WHERE job_application_id = %s",
            (application_id,)
        )
        conn.commit()
        return {"success": True, "application_id": application_id, "status": "ACCEPTED"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()


# ── PUT /applications/{application_id}/reject ─────────────────────────────────
@router.put("/applications/{application_id}/reject")
def reject_application(application_id: int):
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)

        cursor.execute(
            "SELECT job_application_id FROM job_applications WHERE job_application_id = %s",
            (application_id,)
        )
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Application not found")

        cursor.execute(
            "UPDATE job_applications SET application_status = 'REJECTED' WHERE job_application_id = %s",
            (application_id,)
        )
        conn.commit()
        return {"success": True, "application_id": application_id, "status": "REJECTED"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()
