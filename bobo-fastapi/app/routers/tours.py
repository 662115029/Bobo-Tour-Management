from fastapi import APIRouter, HTTPException
from app.db.connection import get_connection, get_cursor
from .utils import format_time, is_tour_cancellable

router = APIRouter(tags=["tours"])


def _upsert_language(cursor, name: str) -> int:
    cursor.execute("INSERT IGNORE INTO languages (language_name) VALUES (%s)", (name,))
    cursor.execute("SELECT language_id FROM languages WHERE language_name = %s", (name,))
    return cursor.fetchone()["language_id"]


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
                "SELECT itinerary_date, place_name, start_time, end_time, note, sequence FROM job_itineraries WHERE job_id = %s ORDER BY sequence, start_time",
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

        em_id = data.get("em_id")
        cursor.execute(
            """
            SELECT em_verify_status FROM em_verification
            WHERE em_id = %s AND is_latest = TRUE
            """,
            (em_id,)
        )
        verify_row = cursor.fetchone()
        if not verify_row or verify_row["em_verify_status"] != "VERIFIED":
            raise HTTPException(
                status_code=403,
                detail="Account not verified. Your account must be verified before creating tours."
            )

        cursor.execute(
            """
            INSERT INTO jobs (em_id, job_title, job_description, job_start_date, job_end_date,
                              job_required_vehicle_type, job_required_seat, job_price)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                em_id,
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
                     p.get("hotel_name") or None, format_time(p.get("pickup_time")),
                     p.get("note") or None),
                )

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
                job_price = %s,
                job_updated_at = NOW()
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
                     p.get("hotel_name") or None, format_time(p.get("pickup_time")),
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

        if not is_tour_cancellable(job["job_status"]):
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


@router.get("/tours/{job_id}/matches")
def get_tour_matches(job_id: str, em_id: str, limit: int = 10):
    """
    Suggested freelancer matches for a tour, based on real profile data:
      - verified + active account
      - vehicle type + seat capacity fits the job requirement
      - availability window covers the job's dates
    Ranked by a match score built from required-language overlap and rating.

    Freelancers who already have an application for this job (invited, applied,
    accepted, or rejected) are always kept in the results — even if a fresh
    scan wouldn't surface them anymore — so the card doesn't disappear from
    under the employer after they act on it (e.g. on page refresh).
    """
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)

        cursor.execute(
            """
            SELECT job_id, job_status, job_start_date, job_end_date,
                   job_required_vehicle_type, job_required_seat, selected_fl_id
            FROM jobs
            WHERE job_id = %s AND em_id = %s
            """,
            (job_id, em_id),
        )
        job = cursor.fetchone()
        if not job:
            raise HTTPException(status_code=404, detail="Tour not found")

        cursor.execute(
            """
            SELECT l.language_id, l.language_name
            FROM job_required_languages jrl
            JOIN languages l ON jrl.language_id = l.language_id
            WHERE jrl.job_id = %s
            """,
            (job_id,),
        )
        required_languages = cursor.fetchall()
        required_language_ids = {r["language_id"] for r in required_languages}

        def score_candidate(cand):
            cursor.execute(
                """
                SELECT l.language_id, l.language_name
                FROM fl_languages fll
                JOIN languages l ON fll.language_id = l.language_id
                WHERE fll.fl_id = %s
                """,
                (cand["fl_id"],),
            )
            fl_langs = cursor.fetchall()
            fl_lang_ids = {r["language_id"] for r in fl_langs}
            matched_langs = [r["language_name"] for r in fl_langs if r["language_id"] in required_language_ids]

            if required_language_ids:
                language_ratio = len(fl_lang_ids & required_language_ids) / len(required_language_ids)
            else:
                language_ratio = 1.0

            rating = float(cand.get("fl_rating_avg") or 0)
            rating_ratio = min(rating / 5.0, 1.0)

            # base 20 for already passing the hard filters (vehicle + availability)
            match_score = round(20 + language_ratio * 50 + rating_ratio * 30)
            match_score = max(0, min(100, match_score))

            reasons = []
            if cand.get("fl_vehicle_type"):
                reasons.append(f"{cand['fl_vehicle_type'].title()} certified")
            if cand.get("is_available"):
                reasons.append("Free on dates")
            if matched_langs:
                reasons.append("Speaks " + ", ".join(matched_langs))
            if rating > 0:
                reasons.append(f"{rating:.1f}★ rating")

            return {
                "fl_id": cand["fl_id"],
                "name": cand["fl_name"],
                "matchScore": match_score,
                "reasons": reasons,
                "rating": rating,
            }

        # 1) Fresh suggestions: eligible freelancers with no existing application for this job yet
        cursor.execute(
            """
            SELECT f.fl_id, f.fl_name, f.fl_rating_avg,
                   fv.fl_vehicle_type, fv.fl_vehicle_seat_capa,
                   TRUE AS is_available
            FROM freelancers f
            JOIN fl_vehicle fv ON fv.fl_id = f.fl_id
            JOIN fl_availability fa ON fa.fl_id = f.fl_id
            WHERE f.fl_verify_status = 'VERIFIED'
              AND f.fl_is_active = TRUE
              AND fv.fl_vehicle_type = %s
              AND fv.fl_vehicle_seat_capa >= %s
              AND fa.is_active = TRUE
              AND fa.fl_available_start_date <= %s
              AND fa.fl_available_end_date >= %s
              AND f.fl_id NOT IN (
                  SELECT fl_id FROM job_applications WHERE job_id = %s
              )
              AND (%s IS NULL OR f.fl_id != %s)
            ORDER BY f.fl_rating_avg DESC
            LIMIT %s
            """,
            (
                job["job_required_vehicle_type"], job["job_required_seat"],
                job["job_start_date"], job["job_end_date"],
                job_id,
                job["selected_fl_id"], job["selected_fl_id"],
                limit,
            ),
        )
        fresh_candidates = cursor.fetchall()

        # 2) Already-engaged: anyone with an existing application for this job — always kept,
        #    scored the same way but without the hard eligibility filters (they're already known)
        cursor.execute(
            """
            SELECT f.fl_id, f.fl_name, f.fl_rating_avg,
                   fv.fl_vehicle_type, fv.fl_vehicle_seat_capa,
                   (fa.is_active = TRUE
                    AND fa.fl_available_start_date <= %s
                    AND fa.fl_available_end_date >= %s) AS is_available
            FROM freelancers f
            LEFT JOIN fl_vehicle fv ON fv.fl_id = f.fl_id
            LEFT JOIN fl_availability fa ON fa.fl_id = f.fl_id
            WHERE f.fl_id IN (
                SELECT fl_id FROM job_applications WHERE job_id = %s
            )
            """,
            (job["job_start_date"], job["job_end_date"], job_id),
        )
        engaged_candidates = cursor.fetchall()

        results = [score_candidate(c) for c in fresh_candidates]
        results += [score_candidate(c) for c in engaged_candidates]

        results.sort(key=lambda r: r["matchScore"], reverse=True)
        return {"items": results}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()


@router.post("/tours/{job_id}/invite")
def invite_freelancer(job_id: str, data: dict):
    """Employer-initiated invite: creates a PENDING job_application awaiting the freelancer's response."""
    conn = None
    try:
        em_id = data.get("em_id")
        fl_id = data.get("fl_id")
        if not em_id or not fl_id:
            raise HTTPException(status_code=400, detail="em_id and fl_id are required.")

        conn = get_connection()
        cursor = get_cursor(conn)

        cursor.execute(
            "SELECT job_id, job_status FROM jobs WHERE job_id = %s AND em_id = %s",
            (job_id, em_id),
        )
        job = cursor.fetchone()
        if not job:
            raise HTTPException(status_code=404, detail="Tour not found")
        if job["job_status"] not in ("OPEN", "PENDING"):
            raise HTTPException(status_code=400, detail="This tour is no longer open for matching.")

        cursor.execute(
            "SELECT fl_verify_status FROM freelancers WHERE fl_id = %s",
            (fl_id,),
        )
        freelancer = cursor.fetchone()
        if not freelancer:
            raise HTTPException(status_code=404, detail="Freelancer not found.")
        if freelancer["fl_verify_status"] != "VERIFIED":
            raise HTTPException(status_code=403, detail="Freelancer must be verified before being invited.")

        cursor.execute(
            "SELECT job_application_id FROM job_applications WHERE job_id = %s AND fl_id = %s",
            (job_id, fl_id),
        )
        if cursor.fetchone():
            raise HTTPException(status_code=409, detail="This freelancer already has an application for this tour.")

        # Only one freelancer can be invited (PENDING) per tour at a time — enforce this
        # server-side too, not just via the frontend button state, to close the race
        # condition where two invites could otherwise be sent back-to-back.
        cursor.execute(
            "SELECT job_application_id FROM job_applications WHERE job_id = %s AND application_status = 'PENDING'",
            (job_id,),
        )
        if cursor.fetchone():
            raise HTTPException(status_code=409, detail="Another invite is already pending for this tour. Wait for a response before inviting someone else.")

        cursor.execute(
            """
            INSERT INTO job_applications (job_id, fl_id, application_status)
            VALUES (%s, %s, 'PENDING')
            """,
            (job_id, fl_id),
        )
        conn.commit()
        return {"success": True, "job_application_id": cursor.lastrowid}
    except HTTPException:
        raise
    except Exception as e:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()