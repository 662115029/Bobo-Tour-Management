from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from app.routers import auth, jobs, employers, freelancers, admin, line_bot, reviews, uploads

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

app.include_router(auth.router)
app.include_router(jobs.router)
app.include_router(employers.router)
app.include_router(freelancers.router)
app.include_router(admin.router)
app.include_router(line_bot.router)
app.include_router(reviews.router)
app.include_router(uploads.router)


@app.get("/")
def root():
    return {"status": "running"}
