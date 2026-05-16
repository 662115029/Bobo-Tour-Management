import os
from fastapi import APIRouter, Request, HTTPException
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FlexSendMessage
from pydantic import BaseModel
from notification import notify_job_matched
from app.db.connection import get_connection, get_cursor

router = APIRouter(tags=["line_bot"])

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))


class NotifyRequest(BaseModel):
    line_user_id: str


@router.post("/webhook")
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


@router.post("/test/notify-match")
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
