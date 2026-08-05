"""
One-off script: creates two rich menus (unregistered / registered) via the
LINE Messaging API, uploads their images, and sets Menu A as the default
for anyone who hasn't linked a specific menu yet.

Run once: python setup_rich_menus.py
Requires: pip install requests --break-system-packages (already in requirements.txt)

Before running:
1. Put your two exported images next to this script:
   - richmenu_a.png  (unregistered, single full-width button)
   - richmenu_b.png  (registered, 3 equal columns)
2. Fill in CHANNEL_ACCESS_TOKEN below (the long-lived token from the
   Messaging API tab — same one already set in Render's env vars).
3. Fill in LIFF_ID (the LINE Login channel's LIFF ID, not the Messaging
   API channel's own LIFF tab).
"""
import requests

CHANNEL_ACCESS_TOKEN = "USNnVdV1IUx4vy8tMS/Ul3Or5XkFswlfkmUGpEH/RGNC2y6fMKcBpb/m2WmvN+h2AWoGpKHl/cUiecOUJAEuMgCQ8eeQt9R+42Gms7+bXmPxJQ61h7Rd9w0AZulRUW2L3aZJHyqMm0tSt4gxCtwiIgdB04t89/1O/w1cDnyilFU="
LIFF_ID = "2010988299-KhiGZeLc"

HEADERS_JSON = {
    "Authorization": f"Bearer {CHANNEL_ACCESS_TOKEN}",
    "Content-Type": "application/json",
}

BASE_URL = f"https://liff.line.me/{LIFF_ID}"


def create_rich_menu(payload):
    res = requests.post(
        "https://api.line.me/v2/bot/richmenu",
        headers=HEADERS_JSON,
        json=payload,
    )
    res.raise_for_status()
    return res.json()["richMenuId"]


def upload_image(rich_menu_id, image_path):
    with open(image_path, "rb") as f:
        image_bytes = f.read()
    content_type = "image/png" if image_path.endswith(".png") else "image/jpeg"
    res = requests.post(
        f"https://api-data.line.me/v2/bot/richmenu/{rich_menu_id}/content",
        headers={
            "Authorization": f"Bearer {CHANNEL_ACCESS_TOKEN}",
            "Content-Type": content_type,
        },
        data=image_bytes,
    )
    res.raise_for_status()


def set_default(rich_menu_id):
    res = requests.post(
        f"https://api.line.me/v2/bot/user/all/richmenu/{rich_menu_id}",
        headers=HEADERS_JSON,
    )
    res.raise_for_status()


# --- Menu A: unregistered — top banner (decorative, no action) + full-width Register row ---
# Canvas 2500x843 (half-size, 2 rows). Top ~40% is the banner (not clickable),
# bottom ~60% is the Register button spanning the full width.
menu_a_payload = {
    "size": {"width": 2500, "height": 843},
    "selected": True,
    "name": "menu-a-unregistered",
    "chatBarText": "Menu",
    "areas": [
        {
            "bounds": {"x": 0, "y": 337, "width": 2500, "height": 506},
            "action": {"type": "uri", "label": "Register", "uri": f"{BASE_URL}"},
        }
    ],
}

# --- Menu B: registered — top banner (decorative, no action) + 3 equal columns below ---
# Canvas 2500x1686. Top ~30% (506px) is the banner (not clickable),
# bottom ~70% (1180px) is split into 3 equal columns.
menu_b_payload = {
    "size": {"width": 2500, "height": 1686},
    "selected": True,
    "name": "menu-b-registered",
    "chatBarText": "Menu",
    "areas": [
        {
            "bounds": {"x": 0, "y": 506, "width": 833, "height": 1180},
            "action": {"type": "uri", "label": "Profile", "uri": f"{BASE_URL}#/profile"},
        },
        {
            "bounds": {"x": 833, "y": 506, "width": 834, "height": 1180},
            "action": {"type": "uri", "label": "Availability", "uri": f"{BASE_URL}#/availability"},
        },
        {
            "bounds": {"x": 1667, "y": 506, "width": 833, "height": 1180},
            "action": {"type": "uri", "label": "Job", "uri": f"{BASE_URL}#/jobs"},
        },
    ],
}

if __name__ == "__main__":
    print("Creating Menu A (unregistered)...")
    menu_a_id = create_rich_menu(menu_a_payload)
    upload_image(menu_a_id, "richmenu_a.png")
    print(f"  richMenuId (A): {menu_a_id}")

    print("Creating Menu B (registered)...")
    menu_b_id = create_rich_menu(menu_b_payload)
    upload_image(menu_b_id, "richmenu_b.png")
    print(f"  richMenuId (B): {menu_b_id}")

    print("Setting Menu A as the default for everyone...")
    set_default(menu_a_id)

    print("\nDone. Save these IDs — Menu B's ID goes into freelancers.py:")
    print(f"RICH_MENU_ID_UNREGISTERED = \"{menu_a_id}\"")
    print(f"RICH_MENU_ID_REGISTERED   = \"{menu_b_id}\"")