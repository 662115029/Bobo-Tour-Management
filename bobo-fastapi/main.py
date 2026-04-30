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
    job_id: str

class DocReviewRequest(BaseModel):
    status: str  # APPROVED or REJECTED
    reviewed_by: str

class BanRequest(BaseModel):
    is_active: bool
    admin_id: str

# =============================================================================
# LINE WEBHOOK
# =============================================================================

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

# =============================================================================
# LINE NOTIFY ENDPOINTS
# =============================================================================

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
def accept_job(job_id: str, request: JobResponseRequest):
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
def decline_job(job_id: str, request: JobResponseRequest):
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

# =============================================================================
# ADMIN
# =============================================================================

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
        total_employers = int(cursor.fetchone()["c"])
        cursor.execute("SELECT COUNT(*) AS c FROM freelancers")
        total_freelancers = int(cursor.fetchone()["c"])
        cursor.execute("SELECT COUNT(*) AS c FROM employers WHERE em_verify_status = 'PENDING'")
        pending_employers = int(cursor.fetchone()["c"])
        cursor.execute("SELECT COUNT(*) AS c FROM freelancers WHERE fl_verify_status = 'PENDING'")
        pending_freelancers = int(cursor.fetchone()["c"])
        cursor.execute("SELECT COUNT(*) AS c FROM jobs WHERE job_status = 'OPEN'")
        open_jobs = int(cursor.fetchone()["c"])
        cursor.execute("SELECT COUNT(*) AS c FROM jobs WHERE job_status = 'IN_PROGRESS'")
        in_progress_jobs = int(cursor.fetchone()["c"])
        cursor.execute("SELECT COUNT(*) AS c FROM jobs WHERE job_status = 'COMPLETED'")
        completed_jobs = int(cursor.fetchone()["c"])
        conn.close()
        return {
            "totalJobs": totalJobs,
            "openJobs": open_jobs,
            "inProgressJobs": in_progress_jobs,
            "completedJobs": completed_jobs,
            "employers": total_employers,
            "freelancers": total_freelancers,
            "pendingVerify": pending_employers + pending_freelancers,
            "pendingEmployers": pending_employers,
            "pendingFreelancers": pending_freelancers,
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/admin/admins")
def admin_admins(limit: int = 50, offset: int = 0):
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute(
            """
            SELECT admin_id, name, status, created_at, updated_at
            FROM admins
            ORDER BY created_at DESC
            LIMIT %s OFFSET %s
            """,
            (limit, offset)
        )
        rows = cursor.fetchall()
        conn.close()
        return {"items": rows, "limit": limit, "offset": offset}
    except Exception as e:
        return {"error": str(e), "items": []}

@app.get("/admin/logs")
def admin_logs(limit: int = 50, offset: int = 0,
               action_type: str = None, target_type: str = None):
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        where = []
        params = []
        if action_type:
            where.append("al.action_type = %s")
            params.append(action_type)
        if target_type:
            where.append("al.target_type = %s")
            params.append(target_type)
        where_clause = ("WHERE " + " AND ".join(where)) if where else ""
        cursor.execute(
            f"""
            SELECT al.log_id, a.name AS admin_name,
                   al.action_type, al.target_type,
                   al.target_id, al.target_name, al.note,
                   al.created_at
            FROM admin_logs al
            JOIN admins a ON al.admin_id = a.admin_id
            {where_clause}
            ORDER BY al.created_at DESC
            LIMIT %s OFFSET %s
            """,
            (*params, limit, offset)
        )
        rows = cursor.fetchall()
        conn.close()
        return {"items": rows, "limit": limit, "offset": offset}
    except Exception as e:
        return {"error": str(e), "items": []}

# =============================================================================
# EMPLOYERS
# =============================================================================

@app.get("/employers")
@app.get("/admin/employers")
def get_employers(limit: int = 50, offset: int = 0):
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute(
            """
            SELECT em_id, em_username, em_name, em_phone, em_address, em_bio,
                   em_profile_image_url, em_verify_status, em_is_active,
                   em_rating_avg, em_created_at, em_updated_at
            FROM employers
            ORDER BY em_updated_at DESC
            LIMIT %s OFFSET %s
            """,
            (limit, offset)
        )
        rows = cursor.fetchall()
        conn.close()
        return {"items": rows, "limit": limit, "offset": offset}
    except Exception as e:
        return {"error": str(e), "items": []}

@app.get("/employers/{em_id}")
def get_employer(em_id: str):
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute(
            """
            SELECT em_id, em_username, em_name, em_phone, em_address, em_bio,
                   em_profile_image_url, em_verify_status, em_is_active,
                   em_rating_avg, em_created_at, em_updated_at
            FROM employers
            WHERE em_id = %s
            """,
            (em_id,)
        )
        row = cursor.fetchone()
        conn.close()
        if not row:
            raise HTTPException(status_code=404, detail="Employer not found")
        return row
    except HTTPException:
        raise
    except Exception as e:
        return {"error": str(e)}

@app.get("/em-bank-accounts")
def get_em_bank_accounts(limit: int = 50, offset: int = 0):
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute(
            """
            SELECT eb.em_bank_account_id, eb.em_id, e.em_name,
                   eb.account_name, eb.account_number, eb.bank_name,
                   eb.is_primary, eb.created_at, eb.updated_at
            FROM em_bank_accounts eb
            JOIN employers e ON eb.em_id = e.em_id
            ORDER BY eb.created_at DESC
            LIMIT %s OFFSET %s
            """,
            (limit, offset)
        )
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
        cursor.execute(
            """
            SELECT ed.em_doc_id, ed.em_id, e.em_name,
                   ed.em_doc_type, ed.file_url, ed.em_doc_status,
                   ed.is_latest, ed.em_uploaded_at,
                   a.name AS reviewed_by_name, ed.reviewed_at
            FROM em_documents ed
            JOIN employers e ON ed.em_id = e.em_id
            LEFT JOIN admins a ON ed.reviewed_by = a.admin_id
            ORDER BY ed.em_uploaded_at DESC
            LIMIT %s OFFSET %s
            """,
            (limit, offset)
        )
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
        cursor.execute(
            """
            SELECT ev.em_verify_id, ev.em_id, e.em_name,
                   ev.em_verify_status, ev.is_latest,
                   ev.em_submitted_at, ev.em_verified_at,
                   a.name AS reviewed_by_name
            FROM em_verification ev
            JOIN employers e ON ev.em_id = e.em_id
            LEFT JOIN admins a ON ev.reviewed_by = a.admin_id
            ORDER BY ev.em_submitted_at DESC
            LIMIT %s OFFSET %s
            """,
            (limit, offset)
        )
        rows = cursor.fetchall()
        conn.close()
        return {"items": rows, "limit": limit, "offset": offset}
    except Exception as e:
        return {"error": str(e), "items": []}

# =============================================================================
# FREELANCERS
# =============================================================================

@app.get("/freelancers")
@app.get("/admin/freelancers")
def get_freelancers(limit: int = 50, offset: int = 0):
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute(
            """
            SELECT fl_id, line_user_id, fl_name, fl_date_of_birth,
                   fl_address, fl_bio, fl_profile_image_url,
                   fl_verify_status, fl_is_active, fl_rating_avg,
                   fl_created_at, fl_updated_at
            FROM freelancers
            ORDER BY fl_updated_at DESC
            LIMIT %s OFFSET %s
            """,
            (limit, offset)
        )
        rows = cursor.fetchall()
        conn.close()
        return {"items": rows, "limit": limit, "offset": offset}
    except Exception as e:
        return {"error": str(e), "items": []}

@app.get("/freelancers/{fl_id}")
def get_freelancer(fl_id: str):
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute(
            """
            SELECT fl_id, line_user_id, fl_name, fl_date_of_birth,
                   fl_address, fl_bio, fl_profile_image_url,
                   fl_verify_status, fl_is_active, fl_rating_avg,
                   fl_created_at, fl_updated_at
            FROM freelancers
            WHERE fl_id = %s
            """,
            (fl_id,)
        )
        row = cursor.fetchone()
        conn.close()
        if not row:
            raise HTTPException(status_code=404, detail="Freelancer not found")
        return row
    except HTTPException:
        raise
    except Exception as e:
        return {"error": str(e)}

@app.get("/fl-bank-accounts")
def get_fl_bank_accounts(limit: int = 50, offset: int = 0):
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute(
            """
            SELECT fb.fl_bank_account_id, fb.fl_id, f.fl_name,
                   fb.account_name, fb.account_number, fb.bank_name,
                   fb.is_primary, fb.created_at, fb.updated_at
            FROM fl_bank_accounts fb
            JOIN freelancers f ON fb.fl_id = f.fl_id
            ORDER BY fb.created_at DESC
            LIMIT %s OFFSET %s
            """,
            (limit, offset)
        )
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
        cursor.execute(
            """
            SELECT fv.fl_vehicle_id, fv.fl_id, f.fl_name,
                   fv.fl_vehicle_type, fv.fl_vehicle_brand, fv.fl_vehicle_model,
                   fv.fl_vehicle_year, fv.fl_vehicle_seat_capa,
                   fv.fl_vehicle_license_plate,
                   fv.fl_vehicle_created_at, fv.fl_vehicle_updated_at
            FROM fl_vehicle fv
            JOIN freelancers f ON fv.fl_id = f.fl_id
            ORDER BY fv.fl_vehicle_created_at DESC
            LIMIT %s OFFSET %s
            """,
            (limit, offset)
        )
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
        cursor.execute(
            """
            SELECT fvi.fl_vehicle_image_id, fvi.fl_vehicle_id,
                   fv.fl_vehicle_brand, fv.fl_vehicle_model,
                   fv.fl_vehicle_license_plate, f.fl_name,
                   fvi.fl_vehicle_image_url, fvi.uploaded_at
            FROM fl_vehicle_images fvi
            JOIN fl_vehicle fv ON fvi.fl_vehicle_id = fv.fl_vehicle_id
            JOIN freelancers f ON fv.fl_id = f.fl_id
            ORDER BY fvi.uploaded_at DESC
            LIMIT %s OFFSET %s
            """,
            (limit, offset)
        )
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
        cursor.execute(
            """
            SELECT fl.fl_language_id, fl.fl_id, f.fl_name,
                   fl.fl_language_name, fl.created_at
            FROM fl_languages fl
            JOIN freelancers f ON fl.fl_id = f.fl_id
            ORDER BY f.fl_name, fl.fl_language_name
            LIMIT %s OFFSET %s
            """,
            (limit, offset)
        )
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
        cursor.execute(
            """
            SELECT fp.fl_area_id, fp.fl_id, f.fl_name,
                   fp.fl_area_name, fp.created_at
            FROM fl_pickup_areas fp
            JOIN freelancers f ON fp.fl_id = f.fl_id
            ORDER BY f.fl_name, fp.fl_area_name
            LIMIT %s OFFSET %s
            """,
            (limit, offset)
        )
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
        cursor.execute(
            """
            SELECT fa.fl_available_id, fa.fl_id, f.fl_name,
                   fa.fl_available_start_date, fa.fl_available_end_date,
                   fa.is_active, fa.created_at, fa.updated_at
            FROM fl_availability fa
            JOIN freelancers f ON fa.fl_id = f.fl_id
            ORDER BY fa.fl_available_start_date DESC
            LIMIT %s OFFSET %s
            """,
            (limit, offset)
        )
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
        cursor.execute(
            """
            SELECT fd.fl_doc_id, fd.fl_id, f.fl_name,
                   fd.fl_doc_type, fd.file_url, fd.fl_doc_status,
                   fd.is_latest, fd.fl_uploaded_at,
                   a.name AS reviewed_by_name, fd.reviewed_at
            FROM fl_documents fd
            JOIN freelancers f ON fd.fl_id = f.fl_id
            LEFT JOIN admins a ON fd.reviewed_by = a.admin_id
            ORDER BY fd.fl_uploaded_at DESC
            LIMIT %s OFFSET %s
            """,
            (limit, offset)
        )
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
        cursor.execute(
            """
            SELECT fv.fl_verify_id, fv.fl_id, f.fl_name,
                   fv.fl_verify_status, fv.is_latest,
                   fv.fl_submitted_at, fv.fl_verified_at,
                   a.name AS reviewed_by_name
            FROM fl_verification fv
            JOIN freelancers f ON fv.fl_id = f.fl_id
            LEFT JOIN admins a ON fv.reviewed_by = a.admin_id
            ORDER BY fv.fl_submitted_at DESC
            LIMIT %s OFFSET %s
            """,
            (limit, offset)
        )
        rows = cursor.fetchall()
        conn.close()
        return {"items": rows, "limit": limit, "offset": offset}
    except Exception as e:
        return {"error": str(e), "items": []}

# =============================================================================
# JOBS
# =============================================================================

@app.get("/jobs")
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

@app.get("/jobs/{job_id}")
def get_job(job_id: str):
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
        conn.close()
        if not row:
            raise HTTPException(status_code=404, detail="Job not found")
        return row
    except HTTPException:
        raise
    except Exception as e:
        return {"error": str(e)}

@app.get("/job-required-languages")
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

@app.get("/job-itineraries")
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

@app.get("/job-passengers")
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

@app.get("/job-expenses")
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

@app.get("/job-applications")
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

@app.get("/job-payments")
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

# =============================================================================
# REVIEWS
# =============================================================================

@app.get("/fl-reviews")
def get_fl_reviews(limit: int = 50, offset: int = 0):
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute(
            """
            SELECT fr.fl_review_id, fr.job_id, j.job_title,
                   fr.em_id, em.em_name AS company,
                   fr.fl_id, f.fl_name AS driver_name,
                   fr.rating, fr.comment, fr.reviewed_at
            FROM fl_reviews fr
            JOIN jobs j ON fr.job_id = j.job_id
            JOIN employers em ON fr.em_id = em.em_id
            JOIN freelancers f ON fr.fl_id = f.fl_id
            ORDER BY fr.reviewed_at DESC
            LIMIT %s OFFSET %s
            """,
            (limit, offset)
        )
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
        cursor.execute(
            """
            SELECT er.em_review_id, er.job_id, j.job_title,
                   er.fl_id, f.fl_name AS driver_name,
                   er.em_id, em.em_name AS company,
                   er.rating, er.comment, er.reviewed_at
            FROM em_reviews er
            JOIN jobs j ON er.job_id = j.job_id
            JOIN freelancers f ON er.fl_id = f.fl_id
            JOIN employers em ON er.em_id = em.em_id
            ORDER BY er.reviewed_at DESC
            LIMIT %s OFFSET %s
            """,
            (limit, offset)
        )
        rows = cursor.fetchall()
        conn.close()
        return {"items": rows, "limit": limit, "offset": offset}
    except Exception as e:
        return {"error": str(e), "items": []}

# =============================================================================
# DOCUMENT REVIEW (PATCH)
# =============================================================================

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
                cursor.execute(
                    """
                    UPDATE fl_verification SET fl_verify_status = 'VERIFIED', fl_verified_at = NOW(),
                    reviewed_by = %s WHERE fl_id = %s AND is_latest = 1
                    """,
                    (body.reviewed_by, doc["fl_id"])
                )
        elif body.status == "REJECTED":
            cursor.execute(
                "UPDATE freelancers SET fl_verify_status = 'NOT_VERIFIED' WHERE fl_id = %s",
                (doc["fl_id"],)
            )
            cursor.execute(
                """
                UPDATE fl_verification SET fl_verify_status = 'NOT_VERIFIED'
                WHERE fl_id = %s AND is_latest = 1
                """,
                (doc["fl_id"],)
            )
        # Log the action
        cursor.execute(
            """
            SELECT f.fl_name, fd.fl_doc_type
            FROM fl_documents fd
            JOIN freelancers f ON fd.fl_id = f.fl_id
            WHERE fd.fl_doc_id = %s
            """,
            (doc_id,)
        )
        doc_info = cursor.fetchone()
        if doc_info:
            action = 'APPROVE_DOCUMENT' if body.status == 'APPROVED' else 'REJECT_DOCUMENT'
            cursor.execute(
                """
                INSERT INTO admin_logs
                    (admin_id, action_type, target_type, target_id, target_name, note)
                VALUES (%s, %s, 'DOCUMENT', %s, %s, %s)
                """,
                (body.reviewed_by, action, doc_id,
                 doc_info["fl_name"], doc_info["fl_doc_type"])
            )
            # If just verified, add VERIFY_FREELANCER log too
            if body.status == "APPROVED":
                cursor.execute(
                    "SELECT COUNT(*) AS c FROM fl_documents WHERE fl_id = %s AND is_latest = 1 AND fl_doc_status != 'APPROVED'",
                    (doc["fl_id"],)
                )
                if cursor.fetchone()["c"] == 0:
                    cursor.execute(
                        "SELECT fl_name FROM freelancers WHERE fl_id = %s",
                        (doc["fl_id"],)
                    )
                    fl_info = cursor.fetchone()
                    cursor.execute(
                        """
                        INSERT INTO admin_logs
                            (admin_id, action_type, target_type, target_id, target_name, note)
                        VALUES (%s, 'VERIFY_FREELANCER', 'FREELANCER', %s, %s, 'All 5 documents approved')
                        """,
                        (body.reviewed_by, doc["fl_id"], fl_info["fl_name"])
                    )
        conn.commit()
        conn.close()
        return {"status": "updated", "doc_id": doc_id, "new_status": body.status}
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        conn.close()
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
                cursor.execute(
                    """
                    UPDATE em_verification SET em_verify_status = 'VERIFIED', em_verified_at = NOW(),
                    reviewed_by = %s WHERE em_id = %s AND is_latest = 1
                    """,
                    (body.reviewed_by, doc["em_id"])
                )
        elif body.status == "REJECTED":
            cursor.execute(
                "UPDATE employers SET em_verify_status = 'NOT_VERIFIED' WHERE em_id = %s",
                (doc["em_id"],)
            )
            cursor.execute(
                """
                UPDATE em_verification SET em_verify_status = 'NOT_VERIFIED'
                WHERE em_id = %s AND is_latest = 1
                """,
                (doc["em_id"],)
            )
        # Log the action
        cursor.execute(
            """
            SELECT e.em_name, ed.em_doc_type
            FROM em_documents ed
            JOIN employers e ON ed.em_id = e.em_id
            WHERE ed.em_doc_id = %s
            """,
            (doc_id,)
        )
        doc_info = cursor.fetchone()
        if doc_info:
            action = 'APPROVE_DOCUMENT' if body.status == 'APPROVED' else 'REJECT_DOCUMENT'
            cursor.execute(
                """
                INSERT INTO admin_logs
                    (admin_id, action_type, target_type, target_id, target_name, note)
                VALUES (%s, %s, 'DOCUMENT', %s, %s, %s)
                """,
                (body.reviewed_by, action, doc_id,
                 doc_info["em_name"], doc_info["em_doc_type"])
            )
            if body.status == "APPROVED":
                cursor.execute(
                    "SELECT COUNT(*) AS c FROM em_documents WHERE em_id = %s AND is_latest = 1 AND em_doc_status != 'APPROVED'",
                    (doc["em_id"],)
                )
                if cursor.fetchone()["c"] == 0:
                    cursor.execute(
                        "SELECT em_name FROM employers WHERE em_id = %s",
                        (doc["em_id"],)
                    )
                    em_info = cursor.fetchone()
                    cursor.execute(
                        """
                        INSERT INTO admin_logs
                            (admin_id, action_type, target_type, target_id, target_name, note)
                        VALUES (%s, 'VERIFY_EMPLOYER', 'EMPLOYER', %s, %s, 'All 5 documents approved')
                        """,
                        (body.reviewed_by, doc["em_id"], em_info["em_name"])
                    )
        conn.commit()
        conn.close()
        return {"status": "updated", "doc_id": doc_id, "new_status": body.status}
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        conn.close()
        return {"error": str(e)}

# =============================================================================
# BAN / UNBAN
# =============================================================================

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
        # Log ban/unban
        cursor.execute("SELECT fl_name FROM freelancers WHERE fl_id = %s", (fl_id,))
        fl_info = cursor.fetchone()
        action = 'UNBAN_USER' if body.is_active else 'BAN_USER'
        cursor.execute(
            """
            INSERT INTO admin_logs
                (admin_id, action_type, target_type, target_id, target_name, note)
            VALUES (%s, %s, 'FREELANCER', %s, %s, NULL)
            """,
            (body.admin_id, action, fl_id, fl_info["fl_name"] if fl_info else fl_id)
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
        # Log ban/unban
        cursor.execute("SELECT em_name FROM employers WHERE em_id = %s", (em_id,))
        em_info = cursor.fetchone()
        action = 'UNBAN_USER' if body.is_active else 'BAN_USER'
        cursor.execute(
            """
            INSERT INTO admin_logs
                (admin_id, action_type, target_type, target_id, target_name, note)
            VALUES (%s, %s, 'EMPLOYER', %s, %s, NULL)
            """,
            (body.admin_id, action, em_id, em_info["em_name"] if em_info else em_id)
        )
        conn.commit()
        conn.close()
        return {"status": "updated", "em_id": em_id, "is_active": body.is_active}
    except HTTPException:
        raise
    except Exception as e:
        return {"error": str(e)}

# =============================================================================
# JOBS DELETE (updated for new schema — no job_customers/job_pickups)
# =============================================================================

@app.delete("/jobs/{job_id}")
def delete_job(job_id: str):
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute("SELECT job_id FROM jobs WHERE job_id = %s", (job_id,))
        if not cursor.fetchone():
            conn.close()
            raise HTTPException(status_code=404, detail="Job not found")

        # Delete in FK-safe order
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
        return {"status": "deleted", "job_id": job_id}
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        conn.close()
        return {"error": str(e)}