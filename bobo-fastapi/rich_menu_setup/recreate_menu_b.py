"""
Recreates Menu B using query-parameter deep links (?target=profile) instead
of hash fragments (#/profile), which get dropped during LIFF's OAuth login
redirect. Deletes the old Menu B and creates a fresh one with the same
image but corrected action URIs. Menu A doesn't need this (it has no
sub-path target — it always just opens the bare LIFF URL).
"""
import requests

TOKEN = "USNnVdV1IUx4vy8tMS/Ul3Or5XkFswlfkmUGpEH/RGNC2y6fMKcBpb/m2WmvN+h2AWoGpKHl/cUiecOUJAEuMgCQ8eeQt9R+42Gms7+bXmPxJQ61h7Rd9w0AZulRUW2L3aZJHyqMm0tSt4gxCtwiIgdB04t89/1O/w1cDnyilFU="
LIFF_ID = "2010988299-KhiGZeLc"
OLD_MENU_B_ID = "richmenu-9005d3bf60b4b4f52b8ee95a472242b9"

BASE_URL = f"https://liff.line.me/{LIFF_ID}"
HEADERS_JSON = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

# 1) Delete the old Menu B
print("Deleting old Menu B...")
requests.delete(f"https://api.line.me/v2/bot/richmenu/{OLD_MENU_B_ID}", headers=HEADERS_JSON)

# 2) Create the new Menu B with query-param deep links
payload = {
    "size": {"width": 2500, "height": 1686},
    "selected": True,
    "name": "menu-b-registered-v2",
    "chatBarText": "Menu",
    "areas": [
        {"bounds": {"x": 0, "y": 506, "width": 833, "height": 1180},
         "action": {"type": "uri", "label": "Profile", "uri": f"{BASE_URL}?target=profile"}},
        {"bounds": {"x": 833, "y": 506, "width": 834, "height": 1180},
         "action": {"type": "uri", "label": "Availability", "uri": f"{BASE_URL}?target=availability"}},
        {"bounds": {"x": 1667, "y": 506, "width": 833, "height": 1180},
         "action": {"type": "uri", "label": "Job", "uri": f"{BASE_URL}?target=jobs"}},
    ],
}
res = requests.post("https://api.line.me/v2/bot/richmenu", headers=HEADERS_JSON, json=payload)
res.raise_for_status()
new_menu_b_id = res.json()["richMenuId"]
print("New Menu B ID:", new_menu_b_id)

# 3) Re-upload the same image (still on disk from before)
print("Uploading image...")
with open("richmenu_b.png", "rb") as f:
    img = f.read()
res2 = requests.post(
    f"https://api-data.line.me/v2/bot/richmenu/{new_menu_b_id}/content",
    headers={"Authorization": f"Bearer {TOKEN}", "Content-Type": "image/png"},
    data=img,
)
print(res2.status_code, res2.text)

print("\nDone. Update RICH_MENU_ID_REGISTERED in freelancers.py to:")
print(f'RICH_MENU_ID_REGISTERED = "{new_menu_b_id}"')