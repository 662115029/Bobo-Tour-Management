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
                   j.area_id AS job_area_id, ar.area_name AS job_area_name,
                   j.job_price, j.job_status,
                   j.selected_fl_id,
                   f.fl_name AS driver_name,
                   f.fl_phone AS driver_phone,
                   f.fl_profile_image_url AS driver_profile_image_url,
                   j.job_created_at, j.job_updated_at
            FROM jobs j
            JOIN employers em ON j.em_id = em.em_id
            LEFT JOIN freelancers f ON j.selected_fl_id = f.fl_id
            LEFT JOIN areas ar ON j.area_id = ar.area_id
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
                area_id = %s,
                job_price = %s,
                job_updated_at = NOW()
            WHERE job_id = %s
            """,
            (
                data.get("job_title"), data.get("job_description"),
                data.get("job_start_date"), data.get("job_end_date"),
                data.get("job_required_vehicle_type", "VAN"),
                data.get("job_required_seat", 9),
                data.get("job_area_id") or None,
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
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)

        cursor.execute(
            """
            SELECT job_id, job_status, job_start_date, job_end_date,
                   job_required_vehicle_type, job_required_seat, selected_fl_id,
                   area_id
            FROM jobs
            WHERE job_id = %s AND em_id = %s
            """,
            (job_id, em_id),
        )
        job = cursor.fetchone()
        if not job:
            raise HTTPException(status_code=404, detail="Tour not found")

        def build_reasons(fl_verify_status, matched_lang_names, covers_area, has_availability):
            reasons = []
            if fl_verify_status == "VERIFIED":
                reasons.append("Verified")
            else:
                reasons.append("Not Verified")
            if has_availability:
                reasons.append("Available on dates")
            else:
                reasons.append("No Availability on Dates")
            if covers_area is True:
                reasons.append("Covers Pickup Area")
            elif covers_area is False:
                reasons.append("Outside Pickup Area")
            # covers_area is None when the job has no required area set — no badge
            if matched_lang_names:
                reasons.append("Speaks " + ", ".join(matched_lang_names))
            return reasons

        # 1) Fresh suggestions: precomputed scores from the Lambda's output table
        cursor.execute(
            """
            SELECT m.fl_id, m.match_score, f.fl_name, f.fl_verify_status, f.fl_rating_avg
            FROM job_fl_matches m
            JOIN freelancers f ON f.fl_id = m.fl_id
            WHERE m.job_id = %s
            ORDER BY m.match_score DESC
            LIMIT %s
            """,
            (job_id, limit),
        )
        fresh_rows = cursor.fetchall()
        fresh_fl_ids = {r["fl_id"] for r in fresh_rows}

        # 2) Already-engaged: anyone with an existing application for this job — always kept,
        #    even if they've dropped out of job_fl_matches (e.g. availability changed since).
        cursor.execute(
            "SELECT DISTINCT fl_id FROM job_applications WHERE job_id = %s",
            (job_id,),
        )
        engaged_fl_ids = {r["fl_id"] for r in cursor.fetchall()}
        missing_engaged_ids = engaged_fl_ids - fresh_fl_ids

        engaged_rows = []
        if missing_engaged_ids:
            fmt = ",".join(["%s"] * len(missing_engaged_ids))
            cursor.execute(
                f"SELECT fl_id, fl_name, fl_verify_status, fl_rating_avg "
                f"FROM freelancers WHERE fl_id IN ({fmt})",
                tuple(missing_engaged_ids),
            )
            engaged_rows = cursor.fetchall()

        # 3) Batch-fetch language info for EVERY candidate (fresh + engaged) in ONE query,
        #    instead of one query per candidate. This is the fix for the slow-loading issue:
        #    previously this ran inside the loop below, turning N candidates into N+ extra
        #    round trips to the database.
        all_fl_ids = fresh_fl_ids | {r["fl_id"] for r in engaged_rows}
        lang_map = {}
        if all_fl_ids:
            fmt = ",".join(["%s"] * len(all_fl_ids))
            cursor.execute(
                f"""
                SELECT fll.fl_id, l.language_name
                FROM fl_languages fll
                JOIN languages l ON l.language_id = fll.language_id
                JOIN job_required_languages jrl
                    ON jrl.language_id = fll.language_id AND jrl.job_id = %s
                WHERE fll.fl_id IN ({fmt})
                """,
                (job_id, *all_fl_ids),
            )
            for row in cursor.fetchall():
                lang_map.setdefault(row["fl_id"], []).append(row["language_name"])

        # 4) Batch-check pickup-area coverage: does each candidate's fl_pickup_areas
        #    include the job's required area? Same batching reasoning as lang_map above.
        #    job["area_id"] is None when the job has no required area set, in which
        #    case we skip the badge entirely rather than showing a misleading result.
        covers_area_fl_ids = set()
        if job["area_id"] and all_fl_ids:
            fmt = ",".join(["%s"] * len(all_fl_ids))
            cursor.execute(
                f"SELECT fl_id FROM fl_pickup_areas WHERE area_id = %s AND fl_id IN ({fmt})",
                (job["area_id"], *all_fl_ids),
            )
            covers_area_fl_ids = {row["fl_id"] for row in cursor.fetchall()}

        # 5) Batch-check real availability overlap with the job's date range.
        #    Same batching reasoning as covers_area_fl_ids above — one query for
        #    every candidate instead of one per candidate in the loop.
        has_availability_fl_ids = set()
        if all_fl_ids:
            fmt = ",".join(["%s"] * len(all_fl_ids))
            cursor.execute(
                f"""
                SELECT fl_id FROM fl_availability
                WHERE fl_id IN ({fmt})
                  AND fl_available_start_date <= %s
                  AND fl_available_end_date   >= %s
                """,
                (*all_fl_ids, job["job_end_date"], job["job_start_date"]),
            )
            has_availability_fl_ids = {row["fl_id"] for row in cursor.fetchall()}

        results = []
        for r in fresh_rows:
            results.append({
                "fl_id": r["fl_id"],
                "name": r["fl_name"],
                "matchScore": float(r["match_score"]),
                "reasons": build_reasons(
                    r["fl_verify_status"], lang_map.get(r["fl_id"], []),
                    (r["fl_id"] in covers_area_fl_ids) if job["area_id"] else None,
                    r["fl_id"] in has_availability_fl_ids
                ),
            })

        for r in engaged_rows:
            # this fl_id isn't in job_fl_matches right now, so no numeric score is
            # available — show them with matchScore=None rather than guessing.
            results.append({
                "fl_id": r["fl_id"],
                "name": r["fl_name"],
                "matchScore": None,
                "reasons": build_reasons(
                    r["fl_verify_status"], lang_map.get(r["fl_id"], []),
                    (r["fl_id"] in covers_area_fl_ids) if job["area_id"] else None,
                    r["fl_id"] in has_availability_fl_ids
                ),
            })

        results.sort(key=lambda r: (r["matchScore"] is None, -(r["matchScore"] or 0)))
        # Cap the combined list at `limit`. Engaged freelancers are still merged in above
        # so they don't vanish just because they fell out of job_fl_matches — but if the
        # total exceeds `limit`, the lowest-scoring entries get dropped first (an engaged
        # freelancer with no score at all counts as the lowest of all).
        results = results[:limit]
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