from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import date

from app.routers import jobs, tours, auth, employers, freelancers, admin, line_bot, reviews, uploads
from app.db.connection import get_connection, get_cursor

load_dotenv()


def update_job_statuses():
    today = date.today()
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)

        # MATCHED → IN_PROGRESS when job_start_date is reached
        cursor.execute(
            """
            UPDATE jobs
            SET job_status = 'IN_PROGRESS', job_updated_at = NOW()
            WHERE job_status = 'MATCHED'
              AND job_start_date <= %s
            """,
            (today,)
        )

        # IN_PROGRESS → COMPLETED when job_end_date has passed AND payment is CONFIRMED
        cursor.execute(
            """
            UPDATE jobs
            SET job_status = 'COMPLETED', job_updated_at = NOW()
            WHERE job_status = 'IN_PROGRESS'
              AND job_end_date < %s
              AND EXISTS (
                SELECT 1 FROM job_payments
                WHERE job_payments.job_id = jobs.job_id
                  AND job_payments.payment_status = 'CONFIRMED'
                  AND job_payments.is_latest = TRUE
              )
            """,
            (today,)
        )

        conn.commit()
        print(f"[Cron] Job statuses updated for {today}")
    except Exception as e:
        print(f"[Cron] Error updating job statuses: {e}")
    finally:
        if conn:
            conn.close()


scheduler = BackgroundScheduler()
scheduler.add_job(update_job_statuses, "cron", hour=0, minute=0)


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.start()
    update_job_statuses()
    yield
    scheduler.shutdown()


app = FastAPI(lifespan=lifespan)

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

app.include_router(auth.router)
app.include_router(uploads.router)
app.include_router(line_bot.router)
app.include_router(admin.router)
app.include_router(employers.router)
app.include_router(freelancers.router)
app.include_router(jobs.router)
app.include_router(tours.router)
app.include_router(reviews.router)


@app.get("/")
def root():
    return {"status": "running"}