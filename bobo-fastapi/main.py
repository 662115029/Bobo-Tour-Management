from fastapi import FastAPI, Request, HTTPException
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FlexSendMessage
from dotenv import load_dotenv
from notification import notify_job_matched, notify_job_confirmed, notify_job_declined
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
import bot

# DB
from app.db.connection import get_connection, get_cursor

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://662115029.github.io",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

class NotifyRequest(BaseModel):
    line_user_id: str

class JobResponseRequest(BaseModel):
    line_user_id: str
    job_id: int

@app.get("/")
def root():
    return {"status": "running"}

@app.post("/webhook")
async def webhook(request: Request):
    signature = request.headers.get("X-Line-Signature")
    body = await request.body()
    try:
        handler.handle(body.decode(), signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")
    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text.lower() == "jobs":
        flex_message = FlexSendMessage(
            alt_text="View available jobs",
            contents={
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {"type": "text", "text": "Bobo Tour Management", "weight": "bold", "size": "xl"},
                        {"type": "text", "text": "Click to view available job listings", "wrap": True}
                    ]
                },
                "footer": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "button",
                            "action": {
                                "type": "uri",
                                "label": "View Jobs",
                                "uri": "https://662115029.github.io/Bobo-Tour-Management/"
                            },
                            "style": "primary"
                        }
                    ]
                }
            }
        )
        line_bot_api.reply_message(event.reply_token, flex_message)
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=event.message.text))

# -----------------------
# LINE NOTIFY ENDPOINTS
# -----------------------

@app.post("/test/notify-match")
def test_notify_match(request: NotifyRequest):
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute(
            """
            SELECT j.job_id, j.job_title, em.em_name, j.job_start_date, j.job_price
            FROM jobs j
            JOIN employers em ON j.em_id = em.em_id
            ORDER BY j.job_created_at DESC
            LIMIT 1
            """
        )
        job = cursor.fetchone()
        conn.close()
        if job:
            notify_job_matched(request.line_user_id, job)
            return {"status": "notification sent", "job": job}
        return {"status": "no jobs found"}
    except Exception as e:
        return {"error": str(e)}

@app.post("/jobs/{job_id}/accept")
def accept_job(job_id: int, request: JobResponseRequest):
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
            notify_job_confirmed(request.line_user_id, job)
        conn.close()
        return {"status": "accepted", "job": job if job else None}
    except Exception as e:
        return {"error": str(e)}

@app.post("/jobs/{job_id}/decline")
def decline_job(job_id: int, request: JobResponseRequest):
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
            notify_job_declined(request.line_user_id, job)
        conn.close()
        return {"status": "declined", "job": job if job else None}
    except Exception as e:
        return {"error": str(e)}


# -----------------------
# JOBS DELETE
# -----------------------

@app.delete("/jobs/{job_id}")
def delete_job(job_id: str):
    try:
        conn = get_connection()
        cursor = get_cursor(conn)

        # Check job exists
        cursor.execute("SELECT job_id FROM jobs WHERE job_id = %s", (job_id,))
        job = cursor.fetchone()
        if not job:
            conn.close()
            raise HTTPException(status_code=404, detail="Job not found")

        # 1. Delete job_customer_pickups (FK -> job_customers + job_pickups)
        cursor.execute("""
            DELETE jcp FROM job_customer_pickups jcp
            JOIN job_customers jc ON jcp.job_customer_id = jc.job_customer_id
            WHERE jc.job_id = %s
        """, (job_id,))

        # 2. Delete job_customers
        cursor.execute("DELETE FROM job_customers WHERE job_id = %s", (job_id,))

        # 3. Delete job_pickups
        cursor.execute("DELETE FROM job_pickups WHERE job_id = %s", (job_id,))

        # 4. Delete job_required_languages
        cursor.execute("DELETE FROM job_required_languages WHERE job_id = %s", (job_id,))

        # 5. Delete job_itineraries
        cursor.execute("DELETE FROM job_itineraries WHERE job_id = %s", (job_id,))

        # 6. Delete job_applications
        cursor.execute("DELETE FROM job_applications WHERE job_id = %s", (job_id,))

        # 7. Delete job_payments
        cursor.execute("DELETE FROM job_payments WHERE job_id = %s", (job_id,))

        # 8. Delete fl_reviews
        cursor.execute("DELETE FROM fl_reviews WHERE job_id = %s", (job_id,))

        # 9. Delete em_reviews
        cursor.execute("DELETE FROM em_reviews WHERE job_id = %s", (job_id,))

        # 10. Delete the job itself
        cursor.execute("DELETE FROM jobs WHERE job_id = %s", (job_id,))

        conn.commit()
        conn.close()
        return {"status": "deleted", "job_id": job_id}
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        conn.close()
        return {"error": str(e)}

# -----------------------
# ADMINS (2 tables)
# -----------------------

@app.get("/admin/db/ping")
def admin_db_ping():
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute("SELECT 1 AS ok")
        row = cursor.fetchone()
        conn.close()
        return {"db": "mysql", "connected": True, "ok": row["ok"]}
    except Exception as e:
        return {"db": "mysql", "connected": False, "error": str(e)}

@app.get("/admin/stats")
def admin_stats():
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute("SELECT COUNT(*) AS c FROM jobs")
        totalJobs = int(cursor.fetchone()["c"])
        cursor.execute("SELECT COUNT(*) AS c FROM employers")
        employers = int(cursor.fetchone()["c"])
        cursor.execute("SELECT COUNT(*) AS c FROM freelancers")
        freelancers = int(cursor.fetchone()["c"])
        cursor.execute("SELECT COUNT(*) AS c FROM employers WHERE em_verify_status = 'PENDING'")
        pending_employers = int(cursor.fetchone()["c"])
        cursor.execute("SELECT COUNT(*) AS c FROM freelancers WHERE fl_verify_status = 'PENDING'")
        pending_freelancers = int(cursor.fetchone()["c"])
        conn.close()
        return {
            "totalJobs": totalJobs,
            "employers": employers,
            "freelancers": freelancers,
            "pendingVerify": pending_employers + pending_freelancers,
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/admin/admins")
def admin_admins(limit: int = 50, offset: int = 0):
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute("SELECT * FROM admins ORDER BY created_at DESC LIMIT %s OFFSET %s", (limit, offset))
        rows = cursor.fetchall()
        conn.close()
        return {"items": rows, "limit": limit, "offset": offset}
    except Exception as e:
        return {"error": str(e), "items": []}

@app.get("/admin/logs")
def admin_logs(limit: int = 50, offset: int = 0):
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute("SELECT * FROM admin_logs ORDER BY created_at DESC LIMIT %s OFFSET %s", (limit, offset))
        rows = cursor.fetchall()
        conn.close()
        return {"items": rows, "limit": limit, "offset": offset}
    except Exception as e:
        return {"error": str(e), "items": []}

# -----------------------
# EMPLOYERS (3 tables)
# -----------------------

@app.get("/employers")
@app.get("/admin/employers")
def get_employers(limit: int = 50, offset: int = 0):
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute("SELECT * FROM employers ORDER BY em_updated_at DESC LIMIT %s OFFSET %s", (limit, offset))
        rows = cursor.fetchall()
        conn.close()
        return {"items": rows, "limit": limit, "offset": offset}
    except Exception as e:
        return {"error": str(e), "items": []}

@app.get("/em-documents")
def get_em_documents(limit: int = 50, offset: int = 0):
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute("SELECT * FROM em_documents ORDER BY em_uploaded_at DESC LIMIT %s OFFSET %s", (limit, offset))
        rows = cursor.fetchall()
        conn.close()
        return {"items": rows, "limit": limit, "offset": offset}
    except Exception as e:
        return {"error": str(e), "items": []}

@app.get("/em-verification")
def get_em_verification(limit: int = 50, offset: int = 0):
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute("SELECT * FROM em_verification ORDER BY em_submitted_at DESC LIMIT %s OFFSET %s", (limit, offset))
        rows = cursor.fetchall()
        conn.close()
        return {"items": rows, "limit": limit, "offset": offset}
    except Exception as e:
        return {"error": str(e), "items": []}

# -----------------------
# FREELANCERS (8 tables)
# -----------------------

@app.get("/freelancers")
@app.get("/admin/freelancers")
def get_freelancers(limit: int = 50, offset: int = 0):
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute("SELECT * FROM freelancers ORDER BY fl_updated_at DESC LIMIT %s OFFSET %s", (limit, offset))
        rows = cursor.fetchall()
        conn.close()
        return {"items": rows, "limit": limit, "offset": offset}
    except Exception as e:
        return {"error": str(e), "items": []}

@app.get("/fl-vehicle")
def get_fl_vehicle(limit: int = 50, offset: int = 0):
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute("SELECT * FROM fl_vehicle LIMIT %s OFFSET %s", (limit, offset))
        rows = cursor.fetchall()
        conn.close()
        return {"items": rows, "limit": limit, "offset": offset}
    except Exception as e:
        return {"error": str(e), "items": []}

@app.get("/fl-vehicle-images")
def get_fl_vehicle_images(limit: int = 50, offset: int = 0):
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute("SELECT * FROM fl_vehicle_images LIMIT %s OFFSET %s", (limit, offset))
        rows = cursor.fetchall()
        conn.close()
        return {"items": rows, "limit": limit, "offset": offset}
    except Exception as e:
        return {"error": str(e), "items": []}

@app.get("/fl-languages")
def get_fl_languages(limit: int = 50, offset: int = 0):
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute("SELECT * FROM fl_languages LIMIT %s OFFSET %s", (limit, offset))
        rows = cursor.fetchall()
        conn.close()
        return {"items": rows, "limit": limit, "offset": offset}
    except Exception as e:
        return {"error": str(e), "items": []}

@app.get("/fl-pickup-areas")
def get_fl_pickup_areas(limit: int = 50, offset: int = 0):
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute("SELECT * FROM fl_pickup_areas LIMIT %s OFFSET %s", (limit, offset))
        rows = cursor.fetchall()
        conn.close()
        return {"items": rows, "limit": limit, "offset": offset}
    except Exception as e:
        return {"error": str(e), "items": []}

@app.get("/fl-availability")
def get_fl_availability(limit: int = 50, offset: int = 0):
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute("SELECT * FROM fl_availability LIMIT %s OFFSET %s", (limit, offset))
        rows = cursor.fetchall()
        conn.close()
        return {"items": rows, "limit": limit, "offset": offset}
    except Exception as e:
        return {"error": str(e), "items": []}

@app.get("/fl-documents")
def get_fl_documents(limit: int = 50, offset: int = 0):
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute("SELECT * FROM fl_documents ORDER BY fl_uploaded_at DESC LIMIT %s OFFSET %s", (limit, offset))
        rows = cursor.fetchall()
        conn.close()
        return {"items": rows, "limit": limit, "offset": offset}
    except Exception as e:
        return {"error": str(e), "items": []}

@app.get("/fl-verification")
def get_fl_verification(limit: int = 50, offset: int = 0):
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute("SELECT * FROM fl_verification ORDER BY fl_submitted_at DESC LIMIT %s OFFSET %s", (limit, offset))
        rows = cursor.fetchall()
        conn.close()
        return {"items": rows, "limit": limit, "offset": offset}
    except Exception as e:
        return {"error": str(e), "items": []}

# -----------------------
# JOBS (8 tables)
# -----------------------

@app.get("/jobs")
def get_jobs(limit: int = 50, offset: int = 0):
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute(
            """
            SELECT j.*, em.em_name AS company
            FROM jobs j
            JOIN employers em ON j.em_id = em.em_id
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

@app.get("/job-required-languages")
def get_job_required_languages(limit: int = 50, offset: int = 0):
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute("SELECT * FROM job_required_languages LIMIT %s OFFSET %s", (limit, offset))
        rows = cursor.fetchall()
        conn.close()
        return {"items": rows, "limit": limit, "offset": offset}
    except Exception as e:
        return {"error": str(e), "items": []}

@app.get("/job-pickups")
def get_job_pickups(limit: int = 50, offset: int = 0):
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute("SELECT * FROM job_pickups ORDER BY job_id, sequence LIMIT %s OFFSET %s", (limit, offset))
        rows = cursor.fetchall()
        conn.close()
        return {"items": rows, "limit": limit, "offset": offset}
    except Exception as e:
        return {"error": str(e), "items": []}

@app.get("/job-customers")
def get_job_customers(limit: int = 50, offset: int = 0):
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute("SELECT * FROM job_customers LIMIT %s OFFSET %s", (limit, offset))
        rows = cursor.fetchall()
        conn.close()
        return {"items": rows, "limit": limit, "offset": offset}
    except Exception as e:
        return {"error": str(e), "items": []}

@app.get("/job-customer-pickups")
def get_job_customer_pickups(limit: int = 50, offset: int = 0):
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute("SELECT * FROM job_customer_pickups LIMIT %s OFFSET %s", (limit, offset))
        rows = cursor.fetchall()
        conn.close()
        return {"items": rows, "limit": limit, "offset": offset}
    except Exception as e:
        return {"error": str(e), "items": []}

@app.get("/job-itineraries")
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

@app.get("/job-applications")
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

@app.get("/job-payments")
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

# -----------------------
# REVIEWS (2 tables)
# -----------------------

@app.get("/fl-reviews")
def get_fl_reviews(limit: int = 50, offset: int = 0):
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute("SELECT * FROM fl_reviews ORDER BY reviewed_at DESC LIMIT %s OFFSET %s", (limit, offset))
        rows = cursor.fetchall()
        conn.close()
        return {"items": rows, "limit": limit, "offset": offset}
    except Exception as e:
        return {"error": str(e), "items": []}

@app.get("/em-reviews")
def get_em_reviews(limit: int = 50, offset: int = 0):
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute("SELECT * FROM em_reviews ORDER BY reviewed_at DESC LIMIT %s OFFSET %s", (limit, offset))
        rows = cursor.fetchall()
        conn.close()
        return {"items": rows, "limit": limit, "offset": offset}
    except Exception as e:
        return {"error": str(e), "items": []}

# -----------------------
# DOCUMENT REVIEW ENDPOINTS
# -----------------------

class DocReviewRequest(BaseModel):
    status: str  # APPROVED or REJECTED
    reviewed_by: str = "ad_001"

@app.patch("/fl-documents/{doc_id}")
def review_fl_document(doc_id: str, body: DocReviewRequest):
    if body.status not in ("APPROVED", "REJECTED"):
        raise HTTPException(status_code=400, detail="status must be APPROVED or REJECTED")
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute("SELECT fl_doc_id, fl_id FROM fl_documents WHERE fl_doc_id = %s", (doc_id,))
        doc = cursor.fetchone()
        if not doc:
            conn.close()
            raise HTTPException(status_code=404, detail="Document not found")
        cursor.execute(
            """
            UPDATE fl_documents
            SET fl_doc_status = %s, reviewed_by = %s, reviewed_at = NOW()
            WHERE fl_doc_id = %s
            """,
            (body.status, body.reviewed_by, doc_id)
        )
        # If all docs for this freelancer are APPROVED, update fl_verify_status
        if body.status == "APPROVED":
            cursor.execute(
                """
                SELECT COUNT(*) AS c FROM fl_documents
                WHERE fl_id = %s AND is_latest = 1 AND fl_doc_status != 'APPROVED'
                """,
                (doc["fl_id"],)
            )
            remaining = cursor.fetchone()["c"]
            if remaining == 0:
                cursor.execute(
                    "UPDATE freelancers SET fl_verify_status = 'VERIFIED' WHERE fl_id = %s",
                    (doc["fl_id"],)
                )
        elif body.status == "REJECTED":
            cursor.execute(
                "UPDATE freelancers SET fl_verify_status = 'NOT_VERIFIED' WHERE fl_id = %s",
                (doc["fl_id"],)
            )
        conn.commit()
        conn.close()
        return {"status": "updated", "doc_id": doc_id, "new_status": body.status}
    except HTTPException:
        raise
    except Exception as e:
        return {"error": str(e)}

@app.patch("/em-documents/{doc_id}")
def review_em_document(doc_id: str, body: DocReviewRequest):
    if body.status not in ("APPROVED", "REJECTED"):
        raise HTTPException(status_code=400, detail="status must be APPROVED or REJECTED")
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute("SELECT em_doc_id, em_id FROM em_documents WHERE em_doc_id = %s", (doc_id,))
        doc = cursor.fetchone()
        if not doc:
            conn.close()
            raise HTTPException(status_code=404, detail="Document not found")
        cursor.execute(
            """
            UPDATE em_documents
            SET em_doc_status = %s, reviewed_by = %s, reviewed_at = NOW()
            WHERE em_doc_id = %s
            """,
            (body.status, body.reviewed_by, doc_id)
        )
        # If all docs for this employer are APPROVED, update em_verify_status
        if body.status == "APPROVED":
            cursor.execute(
                """
                SELECT COUNT(*) AS c FROM em_documents
                WHERE em_id = %s AND is_latest = 1 AND em_doc_status != 'APPROVED'
                """,
                (doc["em_id"],)
            )
            remaining = cursor.fetchone()["c"]
            if remaining == 0:
                cursor.execute(
                    "UPDATE employers SET em_verify_status = 'VERIFIED' WHERE em_id = %s",
                    (doc["em_id"],)
                )
        elif body.status == "REJECTED":
            cursor.execute(
                "UPDATE employers SET em_verify_status = 'NOT_VERIFIED' WHERE em_id = %s",
                (doc["em_id"],)
            )
        conn.commit()
        conn.close()
        return {"status": "updated", "doc_id": doc_id, "new_status": body.status}
    except HTTPException:
        raise
    except Exception as e:
        return {"error": str(e)}
# -----------------------
# BAN / UNBAN ENDPOINTS
# -----------------------

class BanRequest(BaseModel):
    is_active: bool

@app.patch("/freelancers/{fl_id}/ban")
def ban_freelancer(fl_id: str, body: BanRequest):
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute("SELECT fl_id FROM freelancers WHERE fl_id = %s", (fl_id,))
        if not cursor.fetchone():
            conn.close()
            raise HTTPException(status_code=404, detail="Freelancer not found")
        cursor.execute(
            "UPDATE freelancers SET fl_is_active = %s WHERE fl_id = %s",
            (body.is_active, fl_id)
        )
        conn.commit()
        conn.close()
        return {"status": "updated", "fl_id": fl_id, "is_active": body.is_active}
    except HTTPException:
        raise
    except Exception as e:
        return {"error": str(e)}

@app.patch("/employers/{em_id}/ban")
def ban_employer(em_id: str, body: BanRequest):
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute("SELECT em_id FROM employers WHERE em_id = %s", (em_id,))
        if not cursor.fetchone():
            conn.close()
            raise HTTPException(status_code=404, detail="Employer not found")
        cursor.execute(
            "UPDATE employers SET em_is_active = %s WHERE em_id = %s",
            (body.is_active, em_id)
        )
        conn.commit()
        conn.close()
        return {"status": "updated", "em_id": em_id, "is_active": body.is_active}
    except HTTPException:
        raise
    except Exception as e:
        return {"error": str(e)}    