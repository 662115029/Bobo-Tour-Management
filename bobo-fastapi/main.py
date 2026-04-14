from fastapi import FastAPI, Request, HTTPException
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FlexSendMessage
from dotenv import load_dotenv
from notification import notify_job_matched, notify_job_confirmed, notify_job_declined
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os

load_dotenv()

app = FastAPI()

# Add this block
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://bobo-tour-management.netlify.app"],
    allow_methods=["*"],
    allow_headers=["*"],
)

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

MOCK_JOB = {
    "id": 1,
    "title": "Chiang Mai City Tour",
    "date": "2026-05-01",
    "time": "08:00",
    "pickup": "Nimman Road, Chiang Mai",
    "destination": "Doi Suthep Temple",
    "passengers": 8,
    "employer": "Bobo Tour Company"
}

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
    if event.message.text == "งาน":
        flex_message = FlexSendMessage(
            alt_text="ดูงานของเรา",
            contents={
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "Bobo Tour Management",
                            "weight": "bold",
                            "size": "xl"
                        },
                        {
                            "type": "text",
                            "text": "คลิกเพื่อดูตำแหน่งงานที่เปิดรับ",
                            "wrap": True
                        }
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
                                "label": "ดูงาน",
                                "uri": "https://bobo-tour-management.netlify.app"
                            },
                            "style": "primary"
                        }
                    ]
                }
            }
        )
        line_bot_api.reply_message(event.reply_token, flex_message)
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text)
        )

@app.post("/test/notify-match")
def test_notify_match(request: NotifyRequest):
    notify_job_matched(request.line_user_id, MOCK_JOB)
    return {"status": "notification sent"}

@app.post("/jobs/{job_id}/accept")
def accept_job(job_id: int, request: JobResponseRequest):
    notify_job_confirmed(request.line_user_id, MOCK_JOB)
    return {"status": "accepted"}

@app.post("/jobs/{job_id}/decline")
def decline_job(job_id: int, request: JobResponseRequest):
    notify_job_declined(request.line_user_id, MOCK_JOB)
    return {"status": "declined"}