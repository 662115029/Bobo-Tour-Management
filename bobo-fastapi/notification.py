from linebot.v3.messaging import (
    ApiClient,
    MessagingApi,
    PushMessageRequest,
    FlexMessage,
    FlexContainer,
    TextMessage,
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


# Bobo Tour theme
BRAND = "#DC2626"
TEXT = "#0F172A"
TEXT_2 = "#64748B"
BORDER = "#E2E8F0"
TONES = {
    # tone: (header background, header text)
    "brand":   ("#DC2626", "#FFFFFF"),
    "success": ("#16A34A", "#FFFFFF"),
    "danger":  ("#FEF2F2", "#B91C1C"),
    "neutral": ("#F1F5F9", "#475569"),
    "warning": ("#FFFBEB", "#B45309"),
}


def _detail_row(label: str, value: str, bold: bool = False):
    return {
        "type": "box",
        "layout": "horizontal",
        "contents": [
            {"type": "text", "text": label, "size": "sm", "color": TEXT_2, "flex": 2},
            {"type": "text", "text": str(value), "size": "sm", "color": TEXT, "flex": 3, "wrap": True,
             "weight": "bold" if bold else "regular", "align": "end"},
        ],
    }


def _header(headline: str, tone: str):
    bg, fg = TONES.get(tone, TONES["brand"])
    return {
        "type": "box",
        "layout": "vertical",
        "backgroundColor": bg,
        "paddingAll": "16px",
        "spacing": "xs",
        "contents": [
            {"type": "text", "text": "BOBO TOUR", "color": fg, "size": "xxs", "weight": "bold"},
            {"type": "text", "text": headline, "color": fg, "size": "lg", "weight": "bold", "wrap": True},
        ],
    }


def _build_job_flex(headline: str, tone: str, job: dict,
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

    # Employer row: round avatar + name
    employer_row = {
        "type": "box",
        "layout": "horizontal",
        "spacing": "md",
        "alignItems": "center",
        "contents": [],
    }
    if employer_photo:
        employer_row["contents"].append({
            "type": "box", "layout": "vertical", "width": "32px", "height": "32px",
            "cornerRadius": "16px", "flex": 0,
            "contents": [{"type": "image", "url": employer_photo, "size": "full", "aspectMode": "cover", "aspectRatio": "1:1"}],
        })
    else:
        employer_row["contents"].append({
            "type": "box", "layout": "vertical", "width": "32px", "height": "32px",
            "cornerRadius": "16px", "backgroundColor": "#FEF2F2", "flex": 0, "justifyContent": "center",
            "contents": [{"type": "text", "text": employer_name[:1].upper(), "color": BRAND,
                          "weight": "bold", "size": "sm", "align": "center"}],
        })
    employer_row["contents"].append({
        "type": "text", "text": employer_name, "size": "sm", "color": TEXT_2,
        "flex": 1, "gravity": "center", "wrap": True,
    })

    bubble = {
        "type": "bubble",
        "header": _header(headline, tone),
        "body": {
            "type": "box",
            "layout": "vertical",
            "paddingAll": "20px",
            "spacing": "md",
            "contents": [
                employer_row,
                {"type": "text", "text": job.get("job_title", ""), "size": "lg", "weight": "bold",
                 "color": TEXT, "wrap": True},
                {"type": "separator", "color": BORDER},
                {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                        _detail_row("Job date", date_range),
                        _detail_row("Pickup area", pickup_area),
                    ],
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "backgroundColor": "#F8FAFC",
                    "cornerRadius": "8px",
                    "paddingAll": "12px",
                    "contents": [
                        {"type": "text", "text": "Rate", "size": "sm", "color": TEXT_2, "gravity": "center"},
                        {"type": "text", "text": price_text, "size": "xl", "weight": "bold",
                         "color": TEXT, "align": "end"},
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
                    "color": BRAND,
                    "height": "sm",
                    "action": {"type": "uri", "label": button_label, "uri": uri},
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
        "📨 Application sent", "brand", job,
        button_label="View application status", button_target="jobs", button_tab="my-request",
    )
    _push_flex(line_user_id, f"You've applied for {job.get('job_title', '')}", bubble)


# ---------------------------------------------------------------------------
# 2. Employer responds to a freelancer's own application
# ---------------------------------------------------------------------------
def notify_application_accepted(line_user_id: str, job: dict):
    bubble = _build_job_flex(
        "✅ Application accepted", "success", job,
        button_label="View my jobs", button_target="jobs", button_tab="my-job",
    )
    _push_flex(line_user_id, f"Your application for {job.get('job_title', '')} was accepted", bubble)


def notify_application_rejected(line_user_id: str, job: dict):
    bubble = _build_job_flex("Application rejected", "danger", job)
    _push_flex(line_user_id, f"Your application for {job.get('job_title', '')} was rejected", bubble)


def notify_application_cancelled(line_user_id: str, job: dict):
    bubble = _build_job_flex("Application cancelled", "neutral", job)
    _push_flex(line_user_id, f"You've cancelled your application for {job.get('job_title', '')}", bubble)


# ---------------------------------------------------------------------------
# 3. Freelancer is invited to a job via matching (employer-initiated)
# ---------------------------------------------------------------------------
def notify_invited(line_user_id: str, job: dict):
    bubble = _build_job_flex(
        "🚐 New job invite", "brand", job,
        button_label="View invite", button_target="jobs", button_tab="job-offer",
    )
    _push_flex(line_user_id, f"You've been invited to {job.get('job_title', '')}", bubble)


# ---------------------------------------------------------------------------
# 4. Freelancer responds to an invite
# ---------------------------------------------------------------------------
def notify_invite_accepted(line_user_id: str, job: dict):
    bubble = _build_job_flex(
        "✅ Job confirmed", "success", job,
        button_label="View my jobs", button_target="jobs", button_tab="my-job",
    )
    _push_flex(line_user_id, f"You've taken {job.get('job_title', '')}", bubble)


def notify_invite_rejected(line_user_id: str, job: dict):
    bubble = _build_job_flex("Invite declined", "neutral", job)
    _push_flex(line_user_id, f"You've declined the invite for {job.get('job_title', '')}", bubble)


# ---------------------------------------------------------------------------
# 5. Account messages (cards, Bobo's voice)
# ---------------------------------------------------------------------------
DOC_LABELS = {
    "PERSONAL_ID": "ID Card",
    "DRIVER_LICENSE": "Driver License",
    "PUBLIC_DRIVER_LICENSE": "Public Driver License",
    "VEHICLE_REGISTRATION": "Vehicle Registration",
    "VEHICLE_INSPECTION": "Vehicle Inspection",
}


def doc_label(doc_type: str) -> str:
    return DOC_LABELS.get(doc_type or "", (doc_type or "Document").replace("_", " ").title())


def _first_name(full_name: str) -> str:
    first = (full_name or "").strip().split(" ")[0]
    return first.capitalize() if first else "there"


def _text(text: str, color: str = TEXT, size: str = "sm", bold: bool = False):
    t = {"type": "text", "text": text, "size": size, "color": color, "wrap": True}
    if bold:
        t["weight"] = "bold"
    return t


def _note_box(text: str, bg: str, color: str, title: str = None):
    contents = []
    if title:
        contents.append({"type": "text", "text": title, "size": "xs", "color": color, "weight": "bold"})
    contents.append({"type": "text", "text": text, "size": "sm", "color": color, "wrap": True})
    return {"type": "box", "layout": "vertical", "backgroundColor": bg, "cornerRadius": "8px",
            "paddingAll": "12px", "spacing": "xs", "contents": contents}


def _account_card(headline: str, tone: str, body: list, button_label: str = None, button_query: str = None):
    bubble = {
        "type": "bubble",
        "header": _header(headline, tone),
        "body": {"type": "box", "layout": "vertical", "paddingAll": "20px", "spacing": "md", "contents": body},
    }
    if button_label and button_query:
        bubble["footer"] = {
            "type": "box", "layout": "vertical", "paddingAll": "12px",
            "contents": [{
                "type": "button", "style": "primary", "color": BRAND, "height": "sm",
                "action": {"type": "uri", "label": button_label, "uri": f"{LIFF_URL}?{button_query}"},
            }],
        }
    return bubble


def notify_registered(line_user_id: str, full_name: str):
    name = _first_name(full_name)
    bubble = _account_card("🎉 Welcome to the Bobo crew!", "success", [
        _text(f"Yay, you're in, {name}! 🐻", bold=True, size="md"),
        _text("Next, go to your Profile to:", color=TEXT_2),
        _text("🚐 Add your vehicle details\n📄 Upload your documents for verification"),
        _note_box("Once our team verifies your account, you'll be able to apply for tour jobs "
                  "and get matched with tours from tour companies.", "#F8FAFC", TEXT_2, "⏳ After verification"),
        _note_box("Don't forget to set your free dates in Availability, so tour companies "
                  "can find you and invite you to work!", "#FFFBEB", "#B45309", "📅 Availability"),
    ], "Go to Profile", "target=profile")
    _push_flex(line_user_id, "Welcome to the Bobo crew! Next, complete your profile.", bubble)


def notify_verified(line_user_id: str, full_name: str):
    name = _first_name(full_name)
    bubble = _account_card("✅ Account verified", "success", [
        _text(f"Great news, {name}! 🐻", bold=True, size="md"),
        _text("You can now apply for tour jobs and get matched with tours from tour companies 🚐",
              color=TEXT_2),
        _note_box("Keep your free dates up to date in Availability so I can match you with more jobs!",
                  "#FFFBEB", "#B45309", "📅 Availability"),
    ], "Browse open tours", "target=jobs&tab=job-opening")
    _push_flex(line_user_id, "Your account is now verified. You can apply for tour jobs!", bubble)


def notify_document_received(line_user_id: str, full_name: str, doc_type: str, status_changed: bool = False):
    name = _first_name(full_name)
    label = doc_label(doc_type)
    body = [
        _text(f"Thanks, {name}! 🐻", bold=True, size="md"),
        _text(f"We've received your {label}. Our team will review it soon ⏳", color=TEXT_2),
    ]
    if status_changed:
        body.append(_note_box("While it's under review, you can't apply for new tour jobs or get matched. "
                              "I'll let you know as soon as it's done.",
                              "#FFFBEB", "#B45309", "Account pending review"))
    bubble = _account_card(f"📄 {label} received", "warning", body, "View my documents", "target=profile")
    _push_flex(line_user_id, f"We've received your {label}. It's now pending review.", bubble)


def notify_document_rejected(line_user_id: str, full_name: str, doc_type: str, reason: str = None):
    name = _first_name(full_name)
    label = doc_label(doc_type)
    body = [_text(f"Hi {name} 🐻 Your {label} didn't pass verification.")]
    if reason:
        body.append(_note_box(reason, "#FEF2F2", "#B91C1C", "Reason"))
    body.append(_text("Please re-upload this document in your Profile 📄", color=TEXT_2))
    bubble = _account_card(f"📄 {label} rejected", "danger", body, "Go to Profile", "target=profile")
    _push_flex(line_user_id, f"Your {label} was rejected. Please re-upload it in Profile.", bubble)


def notify_not_verified(line_user_id: str, full_name: str):
    name = _first_name(full_name)
    bubble = _account_card("❌ Account not verified", "danger", [
        _text(f"Hi {name} 🐻", bold=True, size="md"),
        _text("Your documents didn't pass verification, so your account is now not verified.", color=TEXT_2),
        _text("Please check your documents in Profile and re-upload them 📄", color=TEXT_2),
    ], "Go to Profile", "target=profile")
    _push_flex(line_user_id, "Your account is not verified. Please check your documents in Profile.", bubble)