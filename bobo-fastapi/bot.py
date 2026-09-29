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
# The welcome message is set in LINE OA Manager (Greeting message),
# so the bot does not reply here to avoid sending it twice.
@handler.add(FollowEvent)
def handle_follow(event):
    pass


# when freelancer sends a message to the bot
@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    api = get_messaging_api()
    text = event.message.text.strip().lower()

    if text in ['job', 'jobs']:
        send_job_list_message(api, event.reply_token)
    else:
        api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[
                    TextMessage(
                        text="Type 'jobs' to see available tour jobs"
                    )
                ]
            )
        )


def send_job_list_message(api, reply_token):
    LIFF_URL = "https://liff.line.me/2010988299-KhiGZeLc"
    flex_content = {
        "type": "bubble",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "Bobo Tour",
                    "color": "#ffffff",
                    "size": "sm"
                },
                {
                    "type": "text",
                    "text": "Available Jobs",
                    "color": "#ffffff",
                    "size": "xl",
                    "weight": "bold"
                }
            ],
            "backgroundColor": "#DC2626",
            "paddingAll": "20px"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "Tour jobs are waiting for you!",
                    "size": "md",
                    "color": "#333333"
                },
                {
                    "type": "text",
                    "text": "Tap the button below to see all job details.",
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
                        "label": "View all jobs",
                        "uri": LIFF_URL
                    },
                    "style": "primary",
                    "color": "#DC2626"
                }
            ],
            "paddingAll": "12px"
        }
    }

    api.reply_message(
        ReplyMessageRequest(
            reply_token=reply_token,
            messages=[
                FlexMessage(
                    alt_text="Available jobs on Bobo Tour",
                    contents=FlexContainer.from_dict(flex_content)
                )
            ]
        )
    )