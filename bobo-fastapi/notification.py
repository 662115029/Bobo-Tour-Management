from linebot.v3.messaging import (
    ApiClient,
    MessagingApi,
    PushMessageRequest,
    TextMessage,
    FlexMessage,
    FlexContainer
)
from bot import configuration

LIFF_URL = "https://liff.line.me/2009771168-w9BjE7bI"


def get_messaging_api():
    return MessagingApi(ApiClient(configuration))


def notify_job_matched(line_user_id: str, job: dict):
    """
    Send a push message to freelancer when they are matched to a job.
    job dict should contain: id, title, date, time, pickup, destination, passengers, employer
    """
    api = get_messaging_api()

    flex_content = {
        "type": "bubble",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "🚐 Bobo Tour",
                    "color": "#ffffff",
                    "size": "sm"
                },
                {
                    "type": "text",
                    "text": "มีงานใหม่สำหรับคุณ!",
                    "color": "#ffffff",
                    "size": "xl",
                    "weight": "bold"
                }
            ],
            "backgroundColor": "#06C755",
            "paddingAll": "20px"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": job["title"],
                    "size": "lg",
                    "weight": "bold",
                    "color": "#333333"
                },
                {
                    "type": "separator",
                    "margin": "md"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "md",
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "📅 วันที่",
                                    "size": "sm",
                                    "color": "#888888",
                                    "flex": 2
                                },
                                {
                                    "type": "text",
                                    "text": job["date"],
                                    "size": "sm",
                                    "color": "#333333",
                                    "flex": 3
                                }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "⏰ เวลา",
                                    "size": "sm",
                                    "color": "#888888",
                                    "flex": 2
                                },
                                {
                                    "type": "text",
                                    "text": job["time"],
                                    "size": "sm",
                                    "color": "#333333",
                                    "flex": 3
                                }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "📍 รับ",
                                    "size": "sm",
                                    "color": "#888888",
                                    "flex": 2
                                },
                                {
                                    "type": "text",
                                    "text": job["pickup"],
                                    "size": "sm",
                                    "color": "#333333",
                                    "flex": 3,
                                    "wrap": True
                                }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "🏁 ส่ง",
                                    "size": "sm",
                                    "color": "#888888",
                                    "flex": 2
                                },
                                {
                                    "type": "text",
                                    "text": job["destination"],
                                    "size": "sm",
                                    "color": "#333333",
                                    "flex": 3,
                                    "wrap": True
                                }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "👥 ผู้โดยสาร",
                                    "size": "sm",
                                    "color": "#888888",
                                    "flex": 2
                                },
                                {
                                    "type": "text",
                                    "text": f"{job['passengers']} คน",
                                    "size": "sm",
                                    "color": "#333333",
                                    "flex": 3
                                }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "🏢 บริษัท",
                                    "size": "sm",
                                    "color": "#888888",
                                    "flex": 2
                                },
                                {
                                    "type": "text",
                                    "text": job["employer"],
                                    "size": "sm",
                                    "color": "#333333",
                                    "flex": 3
                                }
                            ]
                        }
                    ]
                }
            ],
            "paddingAll": "20px"
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
                {
                    "type": "button",
                    "action": {
                        "type": "uri",
                        "label": "ดูรายละเอียดและตอบรับ",
                        "uri": f"{LIFF_URL}/jobs/{job['id']}"
                    },
                    "style": "primary",
                    "color": "#06C755"
                },
                {
                    "type": "text",
                    "text": "กรุณาตอบรับภายใน 24 ชั่วโมง",
                    "size": "xs",
                    "color": "#aaaaaa",
                    "align": "center",
                    "margin": "sm"
                }
            ],
            "paddingAll": "12px"
        }
    }

    api.push_message(
        PushMessageRequest(
            to=line_user_id,
            messages=[
                FlexMessage(
                    alt_text=f"มีงานใหม่สำหรับคุณ: {job['title']}",
                    contents=FlexContainer.from_dict(flex_content)
                )
            ]
        )
    )


def notify_job_confirmed(line_user_id: str, job: dict):
    """
    Confirm to freelancer that their acceptance was recorded.
    """
    api = get_messaging_api()
    api.push_message(
        PushMessageRequest(
            to=line_user_id,
            messages=[
                TextMessage(
                    text=(
                        f"✅ ยืนยันแล้ว!\n\n"
                        f"คุณได้รับงาน: {job['title']}\n"
                        f"วันที่: {job['date']} เวลา {job['time']}\n\n"
                        f"นายจ้างจะติดต่อกลับเร็วๆ นี้ครับ"
                    )
                )
            ]
        )
    )


def notify_job_declined(line_user_id: str, job: dict):
    """
    Confirm to freelancer that their decline was recorded.
    """
    api = get_messaging_api()
    api.push_message(
        PushMessageRequest(
            to=line_user_id,
            messages=[
                TextMessage(
                    text=(
                        f"รับทราบครับ\n\n"
                        f"คุณได้ปฏิเสธงาน: {job['title']}\n"
                        f"ระบบจะหาผู้ขับรายอื่นให้ครับ 👍"
                    )
                )
            ]
        )
    )