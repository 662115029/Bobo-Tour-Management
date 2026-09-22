from linebot.v3.messaging import (
    ApiClient,
    MessagingApi,
    PushMessageRequest,
    FlexMessage,
    FlexContainer
)
from bot import configuration

LIFF_URL = "https://liff.line.me/2010988299-KhiGZeLc"


def get_messaging_api():
    return MessagingApi(ApiClient(configuration))


def _format_date_range(start, end):
    """start/end may be date/datetime objects or 'YYYY-MM-DD' strings."""
    def fmt(d):
        if d is None:
            return "-"
        if hasattr(d, "strftime"):
            return d.strftime("%d %b %Y")
        return str(d)
    s, e = fmt(start), fmt(end)
    return s if s == e else f"{s} - {e}"


def _format_price(price):
    if price is None:
        return "-"
    try:
        return f"\u0e3f{float(price):,.0f}"
    except (TypeError, ValueError):
        return f"\u0e3f{price}"


def _detail_row(label: str, value: str):
    return {
        "type": "box",
        "layout": "horizontal",
        "contents": [
            {"type": "text", "text": label, "size": "sm", "color": "#888888", "flex": 2},
            {"type": "text", "text": str(value), "size": "sm", "color": "#333333", "flex": 3, "wrap": True},
        ],
    }


def _build_job_flex(headline: str, header_color: str, job: dict,
                     button_label: str = None, button_target: str = None, button_tab: str = None):
    """
    job dict fields used: job_id, job_title, job_start_date, job_end_date,
    job_price, em_name, em_profile_image_url, pickup_area
    """
    date_range = _format_date_range(job.get("job_start_date"), job.get("job_end_date"))
    pickup_area = job.get("pickup_area") or "-"
    price_text = _format_price(job.get("job_price"))
    employer_name = job.get("em_name") or "-"
    employer_photo = job.get("em_profile_image_url")

    employer_row = {
        "type": "box",
        "layout": "horizontal",
        "spacing": "sm",
        "alignItems": "center",
        "margin": "sm",
        "contents": [],
    }
    if employer_photo:
        employer_row["contents"].append({
            "type": "image",
            "url": employer_photo,
            "size": "xxs",
            "aspectMode": "cover",
            "flex": 0,
        })
    employer_row["contents"].append({
        "type": "text",
        "text": employer_name,
        "size": "sm",
        "color": "#333333",
        "flex": 1,
        "gravity": "center",
        "wrap": True,
    })

    bubble = {
        "type": "bubble",
        "header": {
            "type": "box",
            "layout": "vertical",
            "backgroundColor": header_color,
            "paddingAll": "16px",
            "contents": [
                {"type": "text", "text": headline, "color": "#ffffff", "size": "md", "weight": "bold", "wrap": True}
            ],
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "paddingAll": "20px",
            "contents": [
                {
                    "type": "text",
                    "text": job.get("job_title", ""),
                    "size": "lg",
                    "weight": "bold",
                    "color": "#333333",
                    "wrap": True,
                },
                {"type": "separator", "margin": "md"},
                {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "md",
                    "spacing": "sm",
                    "contents": [
                        _detail_row("Job date", date_range),
                        _detail_row("Pickup area", pickup_area),
                        _detail_row("Pay", price_text),
                        employer_row,
                    ],
                },
            ],
        },
    }

    if button_label and button_target:
        uri = f"{LIFF_URL}?target={button_target}"
        if button_tab:
            uri += f"&tab={button_tab}"
        bubble["footer"] = {
            "type": "box",
            "layout": "vertical",
            "paddingAll": "12px",
            "contents": [
                {
                    "type": "button",
                    "style": "primary",
                    "color": header_color,
                    "action": {
                        "type": "uri",
                        "label": button_label,
                        "uri": uri,
                    },
                }
            ],
        }

    return bubble


def _push_flex(line_user_id: str, alt_text: str, bubble: dict):
    api = get_messaging_api()
    api.push_message(
        PushMessageRequest(
            to=line_user_id,
            messages=[FlexMessage(alt_text=alt_text[:400], contents=FlexContainer.from_dict(bubble))],
        )
    )


# ---------------------------------------------------------------------------
# 1. Freelancer self-applies to a job
# ---------------------------------------------------------------------------
def notify_applied(line_user_id: str, job: dict):
    bubble = _build_job_flex(
        "Application sent", "#06C755", job,
        button_label="View application status", button_target="jobs", button_tab="my-request",
    )
    _push_flex(line_user_id, f"You've applied for {job.get('job_title', '')}", bubble)


# ---------------------------------------------------------------------------
# 2. Employer responds to a freelancer's own application
# ---------------------------------------------------------------------------
def notify_application_accepted(line_user_id: str, job: dict):
    bubble = _build_job_flex(
        "Application accepted", "#06C755", job,
        button_label="View my jobs", button_target="jobs", button_tab="my-job",
    )
    _push_flex(line_user_id, f"Your application for {job.get('job_title', '')} was accepted", bubble)


def notify_application_rejected(line_user_id: str, job: dict):
    bubble = _build_job_flex("Application rejected", "#E24B4A", job)
    _push_flex(line_user_id, f"Your application for {job.get('job_title', '')} was rejected", bubble)


def notify_application_cancelled(line_user_id: str, job: dict):
    bubble = _build_job_flex("Application cancelled", "#888888", job)
    _push_flex(line_user_id, f"You've cancelled your application for {job.get('job_title', '')}", bubble)


# ---------------------------------------------------------------------------
# 3. Freelancer is invited to a job via matching (employer-initiated)
# ---------------------------------------------------------------------------
def notify_invited(line_user_id: str, job: dict):
    bubble = _build_job_flex(
        "New job invite", "#06C755", job,
        button_label="View invite", button_target="jobs", button_tab="job-offer",
    )
    _push_flex(line_user_id, f"You've been invited to {job.get('job_title', '')}", bubble)


# ---------------------------------------------------------------------------
# 4. Freelancer responds to an invite
# ---------------------------------------------------------------------------
def notify_invite_accepted(line_user_id: str, job: dict):
    bubble = _build_job_flex(
        "Job confirmed", "#06C755", job,
        button_label="View my jobs", button_target="jobs", button_tab="my-job",
    )
    _push_flex(line_user_id, f"You've taken {job.get('job_title', '')}", bubble)


def notify_invite_rejected(line_user_id: str, job: dict):
    bubble = _build_job_flex("Invite declined", "#888888", job)
    _push_flex(line_user_id, f"You've declined the invite for {job.get('job_title', '')}", bubble)