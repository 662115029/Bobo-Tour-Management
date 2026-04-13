from linebot.v3 import WebhookHandler
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
    FlexMessage,
    FlexContainer
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent,
    FollowEvent
)
import os
from dotenv import load_dotenv

load_dotenv()

configuration = Configuration(
    access_token=os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
)
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))


def get_messaging_api():
    return MessagingApi(ApiClient(configuration))


# when freelancer adds the bot as friend
@handler.add(FollowEvent)
def handle_follow(event):
    api = get_messaging_api()
    api.reply_message(
        ReplyMessageRequest(
            reply_token=event.reply_token,
            messages=[
                TextMessage(
                    text=(
                        "สวัสดีครับ! ยินดีต้อนรับสู่ Bobo Tour 🚐\n\n"
                        "คุณสามารถใช้บอทนี้เพื่อ:\n"
                        "• รับการแจ้งเตือนงานใหม่\n"
                        "• ดูงานที่มีอยู่\n"
                        "• ยืนยันหรือปฏิเสธงาน\n\n"
                        "พิมพ์ 'งาน' เพื่อดูงานที่มีอยู่"
                    )
                )
            ]
        )
    )


# when freelancer sends a message to the bot
@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    api = get_messaging_api()
    text = event.message.text.strip().lower()

    if text in ['งาน', 'job', 'jobs', 'หางาน']:
        send_job_list_message(api, event.reply_token)
    else:
        api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[
                    TextMessage(
                        text="พิมพ์ 'งาน' เพื่อดูงานที่มีอยู่ครับ 😊"
                    )
                ]
            )
        )


def send_job_list_message(api, reply_token):
    # this is a Flex Message — a rich card with a button
    # the button opens your LIFF app
    LIFF_URL = "https://liff.line.me/2009771168-w9BjE7bI"

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
                    "text": "งานที่มีอยู่",
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
                    "text": "มีงานรอคุณอยู่!",
                    "size": "md",
                    "color": "#333333"
                },
                {
                    "type": "text",
                    "text": "กดปุ่มด้านล่างเพื่อดูรายละเอียดงานทั้งหมด",
                    "size": "sm",
                    "color": "#888888",
                    "wrap": True,
                    "margin": "md"
                }
            ],
            "paddingAll": "20px"
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "button",
                    "action": {
                        "type": "uri",
                        "label": "ดูงานทั้งหมด",
                        "uri": LIFF_URL
                    },
                    "style": "primary",
                    "color": "#06C755"
                }
            ],
            "paddingAll": "12px"
        }
    }

    api.reply_message(
        ReplyMessageRequest(
            reply_token=event.reply_token,
            messages=[
                FlexMessage(
                    alt_text="งานที่มีอยู่ใน Bobo Tour",
                    contents=FlexContainer.from_dict(flex_content)
                )
            ]
        )
    )