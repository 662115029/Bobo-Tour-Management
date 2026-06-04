from fastapi import APIRouter, HTTPException, Header
from typing import Optional
from app.db.connection import get_connection, get_cursor

router = APIRouter(tags=["jobs"])


@router.get("/jobs")
def get_jobs(
    limit: int = 50,
    offset: int = 0,
    fl_id: Optional[int] = None,
    em_id: Optional[int] = None,
    status: Optional[str] = None,
    year: Optional[int] = None,
    month: Optional[str] = None,
    search: Optional[str] = None,
    sort_by: Optional[str] = None,
    sort_order: Optional[str] = "desc",
):
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        where = []
        params = []
        if fl_id:
            where.append("j.selected_fl_id = %s")
            params.append(fl_id)
        if em_id:
            where.append("j.em_id = %s")
            params.append(em_id)
        if status:
            where.append("j.job_status = %s")
            params.append(status)
        if year:
            where.append("YEAR(j.job_start_date) = %s")
            params.append(year)
        if month:
            where.append("MONTH(j.job_start_date) = %s")
            params.append(int(month))
        if search:
            where.append("j.job_title LIKE %s")
            params.append(f"%{search}%")
        where_sql = ("WHERE " + " AND ".join(where)) if where else ""

        allowed_sort = {
            "job_start_date": "j.job_start_date",
            "job_updated_at": "j.job_updated_at",
            "job_created_at": "j.job_created_at",
            "job_title": "j.job_title",
            "job_price": "j.job_price",
            "em_name": "em.em_name",
        }
        sort_col = allowed_sort.get(sort_by, "j.job_updated_at")
        order = "ASC" if sort_order == "asc" else "DESC"

        params += [limit, offset]
        cursor.execute(
            f"""
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
            {where_sql}
            ORDER BY {sort_col} {order}
            LIMIT %s OFFSET %s
            """,
            params,
        )
        rows = cursor.fetchall()
        return {"items": rows, "limit": limit, "offset": offset}
    except Exception as e:
        return {"error": str(e), "items": []}
    finally:
        if conn:
            conn.close()


@router.get("/jobs/{job_id}")
def get_job(job_id: str):
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
            WHERE j.job_id = %s
            """,
            (job_id,)
        )
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Job not found")
        return row
    except HTTPException:
        raise
    except Exception as e:
        return {"error": str(e)}
    finally:
        if conn:
            conn.close()


@router.post("/jobs")
def create_job(data: dict):
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)

        job_id = data.get("job_id")
        em_id = data.get("em_id")
        job_title = data.get("job_title")
        job_description = data.get("job_description")
        job_start_date = data.get("job_start_date")
        job_end_date = data.get("job_end_date")
        job_required_vehicle_type = data.get("job_required_vehicle_type", "VAN")
        job_required_seat = data.get("job_required_seat", 9)
        job_price = data.get("job_price", 0)
        driver_name = data.get("driver_name")
        driver_phone = data.get("driver_phone")

        cursor.execute(
            """
            INSERT INTO jobs (job_id, em_id, job_title, job_description, job_start_date, job_end_date,
                              job_required_vehicle_type, job_required_seat, job_price, driver_name, driver_phone)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (job_id, em_id, job_title, job_description, job_start_date, job_end_date,
             job_required_vehicle_type, job_required_seat, job_price, driver_name, driver_phone),
        )

        for lang in data.get("job_required_languages", []):
            cursor.execute(
                "INSERT INTO job_required_languages (job_req_lg_id, job_id, language_name) VALUES (%s, %s, %s)",
                (f"LG{job_id[-6:]}", job_id, lang),
            )

        for idx, it in enumerate(data.get("job_itineraries", [])):
            if it.get("place_name"):
                cursor.execute(
                    """
                    INSERT INTO job_itineraries (job_itinerary_id, job_id, place_name, start_time, end_time, note)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (f"IT{job_id[-6:]}{idx}", job_id, it.get("place_name"),
                     it.get("start_time"), it.get("end_time"), it.get("note")),
                )

        for idx, p in enumerate(data.get("job_pickups", [])):
            if p.get("pickup_location"):
                cursor.execute(
                    """
                    INSERT INTO job_pickups (job_pickup_id, job_id, hotel_name, pickup_location, pickup_time, sequence)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (f"PK{job_id[-6:]}{idx}", job_id, p.get("hotel_name"),
                     p.get("pickup_location"), p.get("pickup_time"), idx + 1),
                )

        for idx, c in enumerate(data.get("job_customers", [])):
            if c.get("customer_name"):
                cursor.execute(
                    """
                    INSERT INTO job_customers (job_customer_id, job_id, customer_name, pax_count, note)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (f"CUS{job_id[-6:]}{idx}", job_id, c.get("customer_name"),
                     c.get("pax_count"), c.get("note")),
                )

        for idx, inc in enumerate(data.get("job_inclusions", [])):
            if inc.get("description"):
                cursor.execute(
                    """
                    INSERT INTO job_inclusions (job_inclusion_id, job_id, inclusion_type, description, sequence)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (f"INC{job_id[-6:]}{idx}", job_id, inc.get("inclusion_type"),
                     inc.get("description"), idx + 1),
                )

        for idx, fee in enumerate(data.get("job_entrance_fees", [])):
            if fee.get("place_name"):
                cursor.execute(
                    """
                    INSERT INTO job_entrance_fees (job_entrance_fee_id, job_id, place_name, thai_price, foreigner_price, sequence)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (f"EF{job_id[-6:]}{idx}", job_id, fee.get("place_name"),
                     fee.get("thai_price"), fee.get("foreigner_price"), idx + 1),
                )

        conn.commit()
        return {"success": True, "job_id": job_id}
    except Exception as e:
        return {"error": str(e)}
    finally:
        if conn:
            conn.close()


@router.get("/job-required-languages")
def get_job_required_languages(limit: int = 50, offset: int = 0, job_id: str = None):
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute(
            """
            SELECT jrl.job_id, j.job_title,
                   l.language_id, l.language_name
            FROM job_required_languages jrl
            JOIN jobs j ON jrl.job_id = j.job_id
            JOIN languages l ON jrl.language_id = l.language_id
            {where}
            ORDER BY l.language_name
            LIMIT %s OFFSET %s
            """.format(where="WHERE jrl.job_id = %s" if job_id else ""),
            ([job_id] if job_id else []) + [limit, offset],
        )
        rows = cursor.fetchall()
        return {"items": rows, "limit": limit, "offset": offset}
    except Exception as e:
        return {"error": str(e), "items": []}
    finally:
        if conn:
            conn.close()


@router.get("/job-pickups")
def get_job_pickups(limit: int = 50, offset: int = 0, job_id: str = None):
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute(
            """
            SELECT jp.job_pickup_id, jp.job_id, j.job_title,
                   jp.hotel_name, jp.pickup_location, jp.pickup_time,
                   jp.sequence, jp.created_at
            FROM job_pickups jp
            JOIN jobs j ON jp.job_id = j.job_id
            {where}
            ORDER BY jp.sequence ASC
            LIMIT %s OFFSET %s
            """.format(where="WHERE jp.job_id = %s" if job_id else ""),
            ([job_id] if job_id else []) + [limit, offset],
        )
        rows = cursor.fetchall()
        return {"items": rows, "limit": limit, "offset": offset}
    except Exception as e:
        return {"error": str(e), "items": []}
    finally:
        if conn:
            conn.close()


@router.get("/job-itineraries")
def get_job_itineraries(limit: int = 50, offset: int = 0, job_id: str = None):
    conn = None
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
            {where}
            ORDER BY ji.job_id, ji.sequence
            LIMIT %s OFFSET %s
            """.format(where="WHERE ji.job_id = %s" if job_id else ""),
            ([job_id] if job_id else []) + [limit, offset],
        )
        rows = cursor.fetchall()
        return {"items": rows, "limit": limit, "offset": offset}
    except Exception as e:
        return {"error": str(e), "items": []}
    finally:
        if conn:
            conn.close()


@router.get("/job-passengers")
def get_job_passengers(limit: int = 50, offset: int = 0, job_id: str = None):
    conn = None
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
            {where}
            ORDER BY jp.job_id, jp.pickup_time
            LIMIT %s OFFSET %s
            """.format(where="WHERE jp.job_id = %s" if job_id else ""),
            ([job_id] if job_id else []) + [limit, offset],
        )
        rows = cursor.fetchall()
        return {"items": rows, "limit": limit, "offset": offset}
    except Exception as e:
        return {"error": str(e), "items": []}
    finally:
        if conn:
            conn.close()


@router.get("/job-expenses")
def get_job_expenses(limit: int = 50, offset: int = 0, job_id: str = None):
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute(
            """
            SELECT je.job_expense_id, je.job_id, j.job_title,
                   je.item_name, je.amount, je.sequence, je.created_at
            FROM job_expenses je
            JOIN jobs j ON je.job_id = j.job_id
            {where}
            ORDER BY je.job_id, je.sequence
            LIMIT %s OFFSET %s
            """.format(where="WHERE je.job_id = %s" if job_id else ""),
            ([job_id] if job_id else []) + [limit, offset],
        )
        rows = cursor.fetchall()
        return {"items": rows, "limit": limit, "offset": offset}
    except Exception as e:
        return {"error": str(e), "items": []}
    finally:
        if conn:
            conn.close()


@router.get("/job-applications")
def get_job_applications(limit: int = 50, offset: int = 0, job_id: str = None):
    conn = None
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
            {where}
            ORDER BY ja.applied_at DESC
            LIMIT %s OFFSET %s
            """.format(where="WHERE ja.job_id = %s" if job_id else ""),
            ([job_id] if job_id else []) + [limit, offset],
        )
        rows = cursor.fetchall()
        return {"items": rows, "limit": limit, "offset": offset}
    except Exception as e:
        return {"error": str(e), "items": []}
    finally:
        if conn:
            conn.close()


@router.get("/job-payments")
def get_job_payments(limit: int = 50, offset: int = 0, job_id: int = None):
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        where = "WHERE jp.is_latest = TRUE"
        params = []
        if job_id:
            where += " AND jp.job_id = %s"
            params.append(job_id)
        params += [limit, offset]
        cursor.execute(
            f"""
            SELECT jp.payment_id, jp.job_id, j.job_title,
                   jp.em_id, em.em_name AS company,
                   jp.fl_id, f.fl_name AS driver_name,
                   jp.is_latest, jp.payment_status,
                   jp.slip_url, jp.reject_reason,
                   jp.paid_at, jp.confirmed_at, jp.updated_at
            FROM job_payments jp
            JOIN jobs j        ON jp.job_id = j.job_id
            JOIN employers em  ON jp.em_id  = em.em_id
            JOIN freelancers f ON jp.fl_id  = f.fl_id
            {where}
            ORDER BY jp.updated_at DESC
            LIMIT %s OFFSET %s
            """,
            params,
        )
        rows = cursor.fetchall()
        return {"items": rows, "limit": limit, "offset": offset}
    except Exception as e:
        return {"error": str(e), "items": []}
    finally:
        if conn:
            conn.close()


@router.get("/job-payments/{job_id}/history")
def get_job_payment_history(job_id: int):
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute(
            """
            SELECT jp.payment_id, jp.job_id, j.job_title,
                   jp.em_id, em.em_name AS company,
                   jp.fl_id, f.fl_name AS driver_name,
                   jp.is_latest, jp.payment_status,
                   jp.slip_url, jp.reject_reason,
                   jp.paid_at, jp.confirmed_at, jp.updated_at
            FROM job_payments jp
            JOIN jobs j        ON jp.job_id = j.job_id
            JOIN employers em  ON jp.em_id  = em.em_id
            JOIN freelancers f ON jp.fl_id  = f.fl_id
            WHERE jp.job_id = %s
            ORDER BY jp.payment_id ASC
            """,
            (job_id,),
        )
        rows = cursor.fetchall()
        return {"job_id": job_id, "history": rows}
    except Exception as e:
        return {"error": str(e), "history": []}
    finally:
        if conn:
            conn.close()


@router.post("/job-payments")
def create_job_payment(data: dict):
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)

        job_id = data.get("job_id")
        em_id = data.get("em_id")
        fl_id = data.get("fl_id")
        slip_url = data.get("slip_url")

        cursor.execute(
            "SELECT payment_id, payment_status FROM job_payments WHERE job_id = %s AND is_latest = TRUE",
            (job_id,),
        )
        existing = cursor.fetchone()
        if existing:
            raise HTTPException(
                status_code=409,
                detail=f"Payment already exists (payment_id={existing['payment_id']}, status={existing['payment_status']}). Use PATCH to reupload after REJECTED.",
            )

        cursor.execute(
            """
            INSERT INTO job_payments
                (job_id, em_id, fl_id, is_latest, payment_status, slip_url, paid_at)
            VALUES (%s, %s, %s, TRUE, 'PENDING', %s, NOW())
            """,
            (job_id, em_id, fl_id, slip_url),
        )
        conn.commit()
        return {"success": True, "payment_id": cursor.lastrowid}
    except HTTPException:
        raise
    except Exception as e:
        if conn:
            conn.rollback()
        return {"error": str(e)}
    finally:
        if conn:
            conn.close()


@router.patch("/job-payments/{job_id}/reupload")
def reupload_job_payment(job_id: int, data: dict):
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)

        cursor.execute(
            "SELECT payment_id, payment_status, em_id, fl_id FROM job_payments WHERE job_id = %s AND is_latest = TRUE",
            (job_id,),
        )
        current = cursor.fetchone()
        if not current:
            raise HTTPException(status_code=404, detail="No active payment found for this job.")
        if current["payment_status"] != "REJECTED":
            raise HTTPException(
                status_code=400,
                detail=f"Cannot reupload. Current payment status is '{current['payment_status']}' (must be REJECTED).",
            )

        slip_url = data.get("slip_url")
        if not slip_url:
            raise HTTPException(status_code=400, detail="slip_url is required.")

        cursor.execute(
            "UPDATE job_payments SET is_latest = NULL WHERE job_id = %s AND is_latest = TRUE",
            (job_id,),
        )
        cursor.execute(
            """
            INSERT INTO job_payments
                (job_id, em_id, fl_id, is_latest, payment_status, slip_url, paid_at)
            VALUES (%s, %s, %s, TRUE, 'PENDING', %s, NOW())
            """,
            (job_id, current["em_id"], current["fl_id"], slip_url),
        )
        conn.commit()
        return {"success": True, "payment_id": cursor.lastrowid, "job_id": job_id}
    except HTTPException:
        raise
    except Exception as e:
        if conn:
            conn.rollback()
        return {"error": str(e)}
    finally:
        if conn:
            conn.close()


@router.patch("/job-payments/{job_id}/review")
def review_job_payment(job_id: int, data: dict):
    conn = None
    try:
        status = data.get("status")
        reject_reason = data.get("reject_reason")

        if status not in ("CONFIRMED", "REJECTED"):
            raise HTTPException(status_code=400, detail="status must be CONFIRMED or REJECTED.")
        if status == "REJECTED" and not reject_reason:
            raise HTTPException(status_code=400, detail="reject_reason is required when rejecting.")

        conn = get_connection()
        cursor = get_cursor(conn)

        cursor.execute(
            "SELECT payment_id FROM job_payments WHERE job_id = %s AND is_latest = TRUE",
            (job_id,),
        )
        current = cursor.fetchone()
        if not current:
            raise HTTPException(status_code=404, detail="No active payment found for this job.")

        if status == "CONFIRMED":
            cursor.execute(
                """
                UPDATE job_payments
                SET payment_status = 'CONFIRMED',
                    confirmed_at   = NOW(),
                    reject_reason  = NULL
                WHERE job_id = %s AND is_latest = TRUE
                """,
                (job_id,),
            )
        else:
            cursor.execute(
                """
                UPDATE job_payments
                SET payment_status = 'REJECTED',
                    reject_reason  = %s,
                    confirmed_at   = NULL
                WHERE job_id = %s AND is_latest = TRUE
                """,
                (reject_reason, job_id),
            )

        conn.commit()
        return {"success": True, "job_id": job_id, "status": status}
    except HTTPException:
        raise
    except Exception as e:
        if conn:
            conn.rollback()
        return {"error": str(e)}
    finally:
        if conn:
            conn.close()


@router.patch("/job-applications/{application_id}/accept")
def accept_application(application_id: int):
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute("SELECT * FROM job_applications WHERE job_application_id = %s", (application_id,))
        app = cursor.fetchone()
        if not app:
            raise HTTPException(status_code=404, detail="Application not found")
        cursor.execute(
            "UPDATE job_applications SET application_status = 'ACCEPTED', updated_at = NOW() WHERE job_application_id = %s",
            (application_id,)
        )
        cursor.execute(
            "UPDATE jobs SET selected_fl_id = %s, job_status = 'MATCHED' WHERE job_id = %s",
            (app["fl_id"], app["job_id"])
        )
        conn.commit()
        return {"success": True}
    except HTTPException:
        raise
    except Exception as e:
        if conn: conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn: conn.close()


@router.patch("/job-applications/{application_id}/reject")
def reject_application(application_id: int):
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute("SELECT job_application_id FROM job_applications WHERE job_application_id = %s", (application_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Application not found")
        cursor.execute(
            "UPDATE job_applications SET application_status = 'REJECTED', updated_at = NOW() WHERE job_application_id = %s",
            (application_id,)
        )
        conn.commit()
        return {"success": True}
    except HTTPException:
        raise
    except Exception as e:
        if conn: conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn: conn.close()


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

        if admin_id:
            log_conn = None
            try:
                log_conn = get_connection()
                log_cursor = get_cursor(log_conn)
                log_cursor.execute(
                    """
                    INSERT INTO admin_logs
                        (admin_id, action_type, target_type, target_id, target_name, note)
                    VALUES (%s, 'DELETE_JOB', 'JOB', %s, %s, NULL)
                    """,
                    (admin_id, job_id, job_title),
                )
                log_conn.commit()
            except Exception as log_error:
                print(f"ERROR inserting log: {str(log_error)}")
            finally:
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
        raise HTTPException(status_code=500, detail=f"Failed to delete job: {str(e)}")
    finally:
        if conn:
            conn.close()