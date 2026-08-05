from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.db.connection import get_connection, get_cursor
from .utils import (
    validate_doc_review_status,
    determine_verify_status,
    sanitize_sort_params,
    validate_language_name,
    validate_freelancer_register_fields,
    validate_profile_update_fields,
    validate_pin,
)
import bcrypt
import os
import requests

router = APIRouter(tags=["freelancers"])

LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
RICH_MENU_ID_REGISTERED = "richmenu-9005d3bf60b4b4f52b8ee95a472242b9"

def link_rich_menu_to_user(line_user_id: str):
    """Switch a user's rich menu to the full (registered) menu after they sign up."""
    if not line_user_id:
        return
    try:
        requests.post(
            f"https://api.line.me/v2/bot/user/{line_user_id}/richmenu/{RICH_MENU_ID_REGISTERED}",
            headers={"Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}"},
            timeout=5,
        )
    except Exception:
        pass  # rich menu switch failing shouldn't block registration

FL_DOC_TYPES = [
    "PERSONAL_ID",
    "DRIVER_LICENSE",
    "PUBLIC_DRIVER_LICENSE",
    "VEHICLE_REGISTRATION",
    "VEHICLE_INSPECTION",
]


class FreelancerRegisterRequest(BaseModel):
    fl_username: str
    fl_email: str
    fl_name: str
    fl_phone: str
    fl_pin: str
    line_user_id: Optional[str] = None


class FreelancerLoginRequest(BaseModel):
    identifier: Optional[str] = None
    line_user_id: Optional[str] = None
    pin: str


class DocReviewRequest(BaseModel):
    status: str
    reviewed_by: str
    note: Optional[str] = None
    reason: Optional[str] = None


class BanRequest(BaseModel):
    is_active: bool
    admin_id: str


class FreelancerProfileUpdateRequest(BaseModel):
    fl_name: Optional[str] = None
    fl_email: Optional[str] = None
    fl_phone: Optional[str] = None
    fl_address: Optional[str] = None
    fl_bio: Optional[str] = None
    fl_date_of_birth: Optional[str] = None
    fl_profile_image_url: Optional[str] = None


class ChangePinRequest(BaseModel):
    current_pin: str
    new_pin: str


class VehicleRequest(BaseModel):
    fl_vehicle_brand: str
    fl_vehicle_model: str
    fl_vehicle_year: int
    fl_vehicle_seat_capa: int
    fl_vehicle_license_plate: str


class AvailabilityRequest(BaseModel):
    fl_id: int
    fl_available_start_date: str
    fl_available_end_date: str


class JobApplicationRequest(BaseModel):
    job_id: int
    fl_id: int


@router.post("/freelancers/register")
def register_freelancer(body: FreelancerRegisterRequest):
    conn = None
    try:
        field_err = validate_freelancer_register_fields(
            body.fl_username, body.fl_name, body.fl_email, body.fl_pin
        )
        if field_err:
            raise HTTPException(status_code=400, detail=field_err)

        conn = get_connection()
        cursor = get_cursor(conn)

        cursor.execute(
            "SELECT fl_id FROM freelancers WHERE fl_email = %s OR fl_username = %s",
            (body.fl_email, body.fl_username)
        )
        if cursor.fetchone():
            raise HTTPException(status_code=409, detail="Email or username already taken.")

        pin_hash = bcrypt.hashpw(body.fl_pin.encode(), bcrypt.gensalt()).decode()

        cursor.execute(
            """
            INSERT INTO freelancers
                (line_user_id, fl_username, fl_email, fl_name, fl_phone, fl_pin_hash,
                 fl_verify_status, fl_is_active)
            VALUES (%s, %s, %s, %s, %s, %s, 'PENDING', 1)
            """,
            (body.line_user_id, body.fl_username,
             body.fl_email, body.fl_name, body.fl_phone, pin_hash)
        )
        fl_id = cursor.lastrowid

        cursor.execute(
            """
            INSERT INTO fl_verification
                (fl_id, fl_verify_status, is_latest)
            VALUES (%s, 'PENDING', 1)
            """,
            (fl_id,)
        )

        for doc_type in FL_DOC_TYPES:
            cursor.execute(
                """
                INSERT INTO fl_documents
                    (fl_id, fl_doc_type, file_url, fl_doc_status)
                VALUES (%s, %s, NULL, 'PENDING')
                """,
                (fl_id, doc_type)
            )

        conn.commit()
        link_rich_menu_to_user(body.line_user_id)
        return {"success": True, "fl_id": fl_id}

    except HTTPException:
        raise
    except Exception as e:
        if conn:
            conn.rollback()
        return {"success": False, "error": str(e)}
    finally:
        if conn:
            conn.close()


@router.post("/freelancers/login")
def freelancer_login(body: FreelancerLoginRequest):
    conn = None
    try:
        if not body.identifier and not body.line_user_id:
            raise HTTPException(status_code=400, detail="identifier or line_user_id is required.")

        conn = get_connection()
        cursor = get_cursor(conn)

        if body.line_user_id:
            cursor.execute(
                """
                SELECT fl_id, fl_username, fl_name, fl_email, fl_pin_hash,
                       fl_profile_image_url, line_user_id
                FROM freelancers WHERE line_user_id = %s
                """,
                (body.line_user_id,)
            )
        else:
            cursor.execute(
                """
                SELECT fl_id, fl_username, fl_name, fl_email, fl_pin_hash,
                       fl_profile_image_url, line_user_id
                FROM freelancers WHERE fl_username = %s OR fl_email = %s
                """,
                (body.identifier, body.identifier)
            )

        freelancer = cursor.fetchone()
        if not freelancer:
            raise HTTPException(status_code=401, detail="Invalid credentials.")
        if not bcrypt.checkpw(body.pin.encode(), freelancer["fl_pin_hash"].encode()):
            raise HTTPException(status_code=401, detail="Invalid credentials.")

        # Auto-link legacy accounts: if this record has no LINE ID on file yet,
        # and we now know it from this login, attach it.
        if body.line_user_id and not freelancer["line_user_id"]:
            cursor.execute(
                "UPDATE freelancers SET line_user_id = %s WHERE fl_id = %s AND line_user_id IS NULL",
                (body.line_user_id, freelancer["fl_id"])
            )
            conn.commit()

        return {
            "fl_id": freelancer["fl_id"],
            "fl_username": freelancer["fl_username"],
            "fl_name": freelancer["fl_name"],
            "fl_email": freelancer["fl_email"],
            "fl_profile_image_url": freelancer["fl_profile_image_url"],
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()

@router.get("/freelancers/by-line/{line_user_id}")
def check_freelancer_by_line(line_user_id: str):
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute(
            "SELECT fl_id FROM freelancers WHERE line_user_id = %s",
            (line_user_id,)
        )
        freelancer = cursor.fetchone()
        return {"exists": freelancer is not None}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()

@router.get("/freelancers")

@router.get("/admin/freelancers")
def get_freelancers(limit: int = 10, offset: int = 0, search: str = "", status: str = "", sort_by: str = "f.fl_updated_at", sort_order: str = "desc"):
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        where = []
        params = []
        if search:
            where.append("(f.fl_name LIKE %s OR f.fl_username LIKE %s)")
            params += [f"%{search}%", f"%{search}%"]
        if status:
            where.append("f.fl_verify_status = %s")
            params.append(status)
        where_sql = "WHERE " + " AND ".join(where) if where else ""
        params += [limit, offset]
        allowed_sort = {"f.fl_name", "f.fl_rating_avg", "f.fl_updated_at", "f.fl_created_at", "fv.fl_submitted_at"}
        safe_sort_by, safe_order = sanitize_sort_params(sort_by, sort_order, allowed_sort, "f.fl_updated_at")
        cursor.execute(
            f"""
            SELECT f.fl_id, f.line_user_id, f.fl_username, f.fl_email, f.fl_name, f.fl_date_of_birth,
                   f.fl_phone, f.fl_address, f.fl_bio, f.fl_profile_image_url,
                   f.fl_verify_status, f.fl_is_active, f.fl_rating_avg,
                   f.fl_created_at, f.fl_updated_at, fv.fl_submitted_at
            FROM freelancers f
            LEFT JOIN fl_verification fv ON fv.fl_id = f.fl_id AND fv.is_latest = 1
            {where_sql}
            ORDER BY {safe_sort_by} {safe_order}
            LIMIT %s OFFSET %s
            """,
            params
        )
        rows = cursor.fetchall()
        return {"items": rows, "limit": limit, "offset": offset, "search": search, "status": status}
    except Exception as e:
        return {"error": str(e), "items": []}
    finally:
        if conn:
            conn.close()
            
@router.get("/freelancers/{fl_id}")
def get_freelancer(fl_id: str):
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute(
            """
            SELECT fl_id, line_user_id, fl_username, fl_email, fl_name, fl_date_of_birth,
                   fl_phone, fl_address, fl_bio, fl_profile_image_url,
                   fl_verify_status, fl_is_active, fl_rating_avg,
                   fl_created_at, fl_updated_at
            FROM freelancers
            WHERE fl_id = %s
            """,
            (fl_id,)
        )
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Freelancer not found")
        return row
    except HTTPException:
        raise
    except Exception as e:
        return {"error": str(e)}
    finally:
        if conn:
            conn.close()


@router.put("/freelancers/{fl_id}")
def update_freelancer(fl_id: str, body: FreelancerProfileUpdateRequest):
    conn = None
    try:
        fields = {k: v for k, v in {
            "fl_name": body.fl_name,
            "fl_email": body.fl_email,
            "fl_phone": body.fl_phone,
            "fl_address": body.fl_address,
            "fl_bio": body.fl_bio,
            "fl_date_of_birth": body.fl_date_of_birth,
        }.items() if v is not None}

        fields_err = validate_profile_update_fields(fields)
        if fields_err and body.fl_profile_image_url is None:
            raise HTTPException(status_code=400, detail=fields_err)

        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute("SELECT fl_id FROM freelancers WHERE fl_id = %s", (fl_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Freelancer not found")

        cursor.execute(
            """
            UPDATE freelancers
            SET fl_name = COALESCE(%s, fl_name),
                fl_email = COALESCE(%s, fl_email),
                fl_phone = COALESCE(%s, fl_phone),
                fl_address = COALESCE(%s, fl_address),
                fl_bio = COALESCE(%s, fl_bio),
                fl_date_of_birth = COALESCE(%s, fl_date_of_birth),
                fl_profile_image_url = COALESCE(%s, fl_profile_image_url)
            WHERE fl_id = %s
            """,
            (body.fl_name, body.fl_email, body.fl_phone, body.fl_address,
             body.fl_bio, body.fl_date_of_birth, body.fl_profile_image_url, fl_id)
        )
        conn.commit()
        return {"status": "updated"}
    except HTTPException:
        raise
    except Exception as e:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()


@router.patch("/freelancers/{fl_id}/pin")
def change_freelancer_pin(fl_id: str, body: ChangePinRequest):
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute("SELECT fl_pin_hash FROM freelancers WHERE fl_id = %s", (fl_id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Freelancer not found")

        if not bcrypt.checkpw(body.current_pin.encode(), row["fl_pin_hash"].encode()):
            raise HTTPException(status_code=401, detail="Current PIN is incorrect.")

        pin_err = validate_pin(body.new_pin)
        if pin_err:
            raise HTTPException(status_code=400, detail=f"New PIN: {pin_err}")

        new_hash = bcrypt.hashpw(body.new_pin.encode(), bcrypt.gensalt()).decode()
        cursor.execute(
            "UPDATE freelancers SET fl_pin_hash = %s WHERE fl_id = %s",
            (new_hash, fl_id)
        )
        conn.commit()
        return {"success": True, "message": "PIN updated successfully."}
    except HTTPException:
        raise
    except Exception as e:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()


@router.get("/fl-bank-accounts")
def get_fl_bank_accounts(limit: int = 10, offset: int = 0, fl_id: Optional[int] = None):
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        where_sql = "WHERE fb.fl_id = %s" if fl_id else ""
        params = ([fl_id] if fl_id else []) + [limit, offset]
        cursor.execute(
            f"""
            SELECT fb.fl_bank_account_id, fb.fl_id, f.fl_name,
                   fb.account_name, fb.account_number, fb.bank_name,
                   fb.is_primary, fb.created_at, fb.updated_at
            FROM fl_bank_accounts fb
            JOIN freelancers f ON fb.fl_id = f.fl_id
            {where_sql}
            ORDER BY fb.created_at DESC
            LIMIT %s OFFSET %s
            """,
            params
        )
        rows = cursor.fetchall()
        return {"items": rows, "limit": limit, "offset": offset}
    except Exception as e:
        return {"error": str(e), "items": []}
    finally:
        if conn:
            conn.close()
@router.get("/fl-vehicle")
def get_fl_vehicle(limit: int = 10, offset: int = 0, fl_id: Optional[int] = None):
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        where_sql = "WHERE fv.fl_id = %s" if fl_id else ""
        params = ([fl_id] if fl_id else []) + [limit, offset]
        cursor.execute(
            f"""
            SELECT fv.fl_vehicle_id, fv.fl_id, f.fl_name,
                   fv.fl_vehicle_type, fv.fl_vehicle_brand, fv.fl_vehicle_model,
                   fv.fl_vehicle_year, fv.fl_vehicle_seat_capa,
                   fv.fl_vehicle_license_plate,
                   fv.fl_vehicle_created_at, fv.fl_vehicle_updated_at
            FROM fl_vehicle fv
            JOIN freelancers f ON fv.fl_id = f.fl_id
            {where_sql}
            ORDER BY fv.fl_vehicle_created_at DESC
            LIMIT %s OFFSET %s
            """,
            params
        )
        rows = cursor.fetchall()
        return {"items": rows, "limit": limit, "offset": offset}
    except Exception as e:
        return {"error": str(e), "items": []}
    finally:
        if conn:
            conn.close()


@router.post("/fl-vehicle")
def create_fl_vehicle(fl_id: int, body: VehicleRequest):
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute("SELECT fl_id FROM freelancers WHERE fl_id = %s", (fl_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Freelancer not found")

        cursor.execute("SELECT fl_vehicle_id FROM fl_vehicle WHERE fl_id = %s", (fl_id,))
        if cursor.fetchone():
            raise HTTPException(status_code=409, detail="Vehicle already exists for this freelancer. Use PUT to update.")

        cursor.execute(
            """
            INSERT INTO fl_vehicle
                (fl_id, fl_vehicle_brand, fl_vehicle_model, fl_vehicle_year,
                 fl_vehicle_seat_capa, fl_vehicle_license_plate)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (fl_id, body.fl_vehicle_brand, body.fl_vehicle_model, body.fl_vehicle_year,
             body.fl_vehicle_seat_capa, body.fl_vehicle_license_plate)
        )
        conn.commit()
        return {"success": True, "fl_vehicle_id": cursor.lastrowid}
    except HTTPException:
        raise
    except Exception as e:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()


@router.put("/fl-vehicle/{vehicle_id}")
def update_fl_vehicle(vehicle_id: str, body: VehicleRequest):
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute("SELECT fl_vehicle_id FROM fl_vehicle WHERE fl_vehicle_id = %s", (vehicle_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Vehicle not found")

        cursor.execute(
            """
            UPDATE fl_vehicle
            SET fl_vehicle_brand = %s, fl_vehicle_model = %s, fl_vehicle_year = %s,
                fl_vehicle_seat_capa = %s, fl_vehicle_license_plate = %s,
                fl_vehicle_updated_at = NOW()
            WHERE fl_vehicle_id = %s
            """,
            (body.fl_vehicle_brand, body.fl_vehicle_model, body.fl_vehicle_year,
             body.fl_vehicle_seat_capa, body.fl_vehicle_license_plate, vehicle_id)
        )
        conn.commit()
        return {"success": True}
    except HTTPException:
        raise
    except Exception as e:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()


@router.delete("/fl-vehicle/{vehicle_id}/images/{image_id}")
def delete_fl_vehicle_image(vehicle_id: str, image_id: str):
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute(
            "SELECT fl_vehicle_image_id FROM fl_vehicle_images WHERE fl_vehicle_image_id = %s AND fl_vehicle_id = %s",
            (image_id, vehicle_id)
        )
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Vehicle image not found")
        cursor.execute("DELETE FROM fl_vehicle_images WHERE fl_vehicle_image_id = %s", (image_id,))
        conn.commit()
        return {"success": True}
    except HTTPException:
        raise
    except Exception as e:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()


@router.get("/fl-vehicle-images")
def get_fl_vehicle_images(limit: int = 10, offset: int = 0, fl_id: Optional[int] = None):
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        where_sql = "WHERE fv.fl_id = %s" if fl_id else ""
        params = ([fl_id] if fl_id else []) + [limit, offset]
        cursor.execute(
            f"""
            SELECT fvi.fl_vehicle_image_id, fvi.fl_vehicle_id,
                   fv.fl_vehicle_brand, fv.fl_vehicle_model,
                   fv.fl_vehicle_license_plate, f.fl_name,
                   fvi.fl_vehicle_image_url, fvi.uploaded_at
            FROM fl_vehicle_images fvi
            JOIN fl_vehicle fv ON fvi.fl_vehicle_id = fv.fl_vehicle_id
            JOIN freelancers f ON fv.fl_id = f.fl_id
            {where_sql}
            ORDER BY fvi.uploaded_at DESC
            LIMIT %s OFFSET %s
            """,
            params
        )
        rows = cursor.fetchall()
        return {"items": rows, "limit": limit, "offset": offset}
    except Exception as e:
        return {"error": str(e), "items": []}
    finally:
        if conn:
            conn.close()
@router.get("/fl-languages")
def get_fl_languages(limit: int = 10, offset: int = 0, fl_id: Optional[int] = None):
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        where_sql = "WHERE fl.fl_id = %s" if fl_id else ""
        params = ([fl_id] if fl_id else []) + [limit, offset]
        cursor.execute(
            f"""
            SELECT fl.fl_id, f.fl_name,
                   l.language_id, l.language_name
            FROM fl_languages fl
            JOIN freelancers f ON fl.fl_id = f.fl_id
            JOIN languages l ON fl.language_id = l.language_id
            {where_sql}
            ORDER BY f.fl_name, l.language_name
            LIMIT %s OFFSET %s
            """,
            params
        )
        rows = cursor.fetchall()
        return {"items": rows, "limit": limit, "offset": offset}
    except Exception as e:
        return {"error": str(e), "items": []}
    finally:
        if conn:
            conn.close()


@router.post("/fl-languages")
def add_fl_language(data: dict):
    conn = None
    try:
        fl_id = data.get("fl_id")
        name, name_err = validate_language_name(data.get("language_name"))
        if name_err:
            raise HTTPException(status_code=400, detail=name_err)
        if not fl_id:
            raise HTTPException(status_code=400, detail="fl_id is required.")

        conn = get_connection()
        cursor = get_cursor(conn)

        cursor.execute(
            "SELECT language_id, language_name FROM languages WHERE LOWER(language_name) = LOWER(%s)",
            (name,)
        )
        lang = cursor.fetchone()
        if not lang:
            cursor.execute("INSERT INTO languages (language_name) VALUES (%s)", (name,))
            language_id = cursor.lastrowid
            language_name = name
        else:
            language_id = lang["language_id"]
            language_name = lang["language_name"]

        cursor.execute(
            "INSERT IGNORE INTO fl_languages (fl_id, language_id) VALUES (%s, %s)",
            (fl_id, language_id)
        )
        conn.commit()
        return {"fl_id": fl_id, "language_id": language_id, "language_name": language_name}
    except HTTPException:
        raise
    except Exception as e:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()


@router.delete("/fl-languages/{fl_id}/{language_id}")
def remove_fl_language(fl_id: str, language_id: str):
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute(
            "DELETE FROM fl_languages WHERE fl_id = %s AND language_id = %s",
            (fl_id, language_id)
        )
        conn.commit()
        return {"success": True}
    except Exception as e:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()


@router.get("/fl-pickup-areas")
def get_fl_pickup_areas(limit: int = 10, offset: int = 0, fl_id: Optional[int] = None):
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        where_sql = "WHERE fp.fl_id = %s" if fl_id else ""
        params = ([fl_id] if fl_id else []) + [limit, offset]
        cursor.execute(
            f"""
            SELECT fp.fl_id, f.fl_name,
                   a.area_id, a.area_name
            FROM fl_pickup_areas fp
            JOIN freelancers f ON fp.fl_id = f.fl_id
            JOIN areas a ON fp.area_id = a.area_id
            {where_sql}
            ORDER BY f.fl_name, a.area_name
            LIMIT %s OFFSET %s
            """,
            params
        )
        rows = cursor.fetchall()
        return {"items": rows, "limit": limit, "offset": offset}
    except Exception as e:
        return {"error": str(e), "items": []}
    finally:
        if conn:
            conn.close()


@router.post("/fl-pickup-areas")
def add_fl_pickup_area(data: dict):
    conn = None
    try:
        fl_id = data.get("fl_id")
        area_name = (data.get("area_name") or "").strip()
        if not area_name:
            raise HTTPException(status_code=400, detail="area_name is required.")
        if not fl_id:
            raise HTTPException(status_code=400, detail="fl_id is required.")

        conn = get_connection()
        cursor = get_cursor(conn)

        cursor.execute(
            "SELECT area_id, area_name FROM areas WHERE LOWER(area_name) = LOWER(%s)",
            (area_name,)
        )
        area = cursor.fetchone()
        if not area:
            cursor.execute("INSERT INTO areas (area_name) VALUES (%s)", (area_name,))
            area_id = cursor.lastrowid
            result_area_name = area_name
        else:
            area_id = area["area_id"]
            result_area_name = area["area_name"]

        cursor.execute(
            "INSERT IGNORE INTO fl_pickup_areas (fl_id, area_id) VALUES (%s, %s)",
            (fl_id, area_id)
        )
        conn.commit()
        return {"fl_id": fl_id, "area_id": area_id, "area_name": result_area_name}
    except HTTPException:
        raise
    except Exception as e:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()


@router.delete("/fl-pickup-areas/{fl_id}/{area_id}")
def remove_fl_pickup_area(fl_id: str, area_id: str):
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute(
            "DELETE FROM fl_pickup_areas WHERE fl_id = %s AND area_id = %s",
            (fl_id, area_id)
        )
        conn.commit()
        return {"success": True}
    except Exception as e:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()


@router.get("/fl-availability")
def get_fl_availability(limit: int = 10, offset: int = 0, fl_id: Optional[int] = None):
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        where_sql = "WHERE fa.fl_id = %s" if fl_id else ""
        params = ([fl_id] if fl_id else []) + [limit, offset]
        cursor.execute(
            f"""
            SELECT fa.fl_available_id, fa.fl_id, f.fl_name,
                   fa.fl_available_start_date, fa.fl_available_end_date,
                   fa.is_active, fa.created_at, fa.updated_at
            FROM fl_availability fa
            JOIN freelancers f ON fa.fl_id = f.fl_id
            {where_sql}
            ORDER BY fa.fl_available_start_date DESC
            LIMIT %s OFFSET %s
            """,
            params
        )
        rows = cursor.fetchall()
        return {"items": rows, "limit": limit, "offset": offset}
    except Exception as e:
        return {"error": str(e), "items": []}
    finally:
        if conn:
            conn.close()


@router.post("/fl-availability")
def save_fl_availability(body: AvailabilityRequest):
    conn = None
    try:
        if body.fl_available_end_date < body.fl_available_start_date:
            raise HTTPException(status_code=400, detail="End date must be on or after the start date.")

        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute("SELECT fl_id FROM freelancers WHERE fl_id = %s", (body.fl_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Freelancer not found")

        cursor.execute("SELECT fl_available_id FROM fl_availability WHERE fl_id = %s", (body.fl_id,))
        existing = cursor.fetchone()

        try:
            if existing:
                cursor.execute(
                    """
                    UPDATE fl_availability
                    SET fl_available_start_date = %s, fl_available_end_date = %s,
                        is_active = TRUE, updated_at = NOW()
                    WHERE fl_id = %s
                    """,
                    (body.fl_available_start_date, body.fl_available_end_date, body.fl_id)
                )
            else:
                cursor.execute(
                    """
                    INSERT INTO fl_availability (fl_id, fl_available_start_date, fl_available_end_date)
                    VALUES (%s, %s, %s)
                    """,
                    (body.fl_id, body.fl_available_start_date, body.fl_available_end_date)
                )
        except Exception as db_err:
            if conn:
                conn.rollback()
            if "chk_availability" in str(db_err).lower() or "constraint" in str(db_err).lower():
                raise HTTPException(
                    status_code=400,
                    detail="Date range must be at most 30 days, with the end date on or after the start date.",
                )
            raise

        conn.commit()
        return {
            "fl_id": body.fl_id,
            "fl_available_start_date": body.fl_available_start_date,
            "fl_available_end_date": body.fl_available_end_date,
        }
    except HTTPException:
        raise
    except Exception as e:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()


@router.get("/fl-documents")
def get_fl_documents(limit: int = 10, offset: int = 0, status: str = "", fl_id: Optional[int] = None, fl_ids: str = ""):
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        where = []
        params = []
        if fl_id:
            where.append("fd.fl_id = %s")
            params.append(fl_id)
        elif fl_ids:
            id_list = [int(i) for i in fl_ids.split(',') if i.strip().isdigit()]
            placeholders = ','.join(['%s'] * len(id_list))
            where.append(f"fd.fl_id IN ({placeholders})")
            params += id_list
        if status:
            where.append("fd.fl_doc_status = %s")
            params.append(status)
        elif not fl_id and not fl_ids:
            where.append("fd.file_url IS NOT NULL")
        where_sql = "WHERE " + " AND ".join(where) if where else ""
        params += [limit, offset]
        cursor.execute(
            f"""
            SELECT fd.fl_doc_id, fd.fl_id, f.fl_name,
                   fd.fl_doc_type, fd.file_url, fd.fl_doc_status,
                   fd.fl_uploaded_at, fd.reject_reason,
                   a.name AS reviewed_by_name, fd.reviewed_at
            FROM fl_documents fd
            JOIN freelancers f ON fd.fl_id = f.fl_id
            LEFT JOIN admins a ON fd.reviewed_by = a.admin_id
            {where_sql}
            ORDER BY fd.fl_uploaded_at ASC
            LIMIT %s OFFSET %s
            """,
            params
        )
        rows = cursor.fetchall()
        return {"items": rows, "limit": limit, "offset": offset}
    except Exception as e:
        return {"error": str(e), "items": []}
    finally:
        if conn:
            conn.close()

@router.get("/fl-verification")
def get_fl_verification(limit: int = 10, offset: int = 0, status: str = "PENDING", fl_id: Optional[int] = None):
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        where = []
        params = []
        if fl_id:
            where.append("fv.fl_id = %s")
            params.append(fl_id)
        if status:
            where.append("fv.fl_verify_status = %s")
            params.append(status)
        where_sql = ("WHERE " + " AND ".join(where)) if where else ""
        params += [limit, offset]
        cursor.execute(
            f"""
            SELECT fv.fl_verify_id, fv.fl_id, f.fl_name,
                   fv.fl_verify_status, fv.is_latest,
                   fv.fl_submitted_at, fv.fl_verified_at,
                   a.name AS reviewed_by_name
            FROM fl_verification fv
            JOIN freelancers f ON fv.fl_id = f.fl_id
            LEFT JOIN admins a ON fv.reviewed_by = a.admin_id
            {where_sql}
            ORDER BY fv.fl_submitted_at ASC
            LIMIT %s OFFSET %s
            """,
            params
        )
        rows = cursor.fetchall()
        return {"items": rows, "limit": limit, "offset": offset}
    except Exception as e:
        return {"error": str(e), "items": []}
    finally:
        if conn:
            conn.close()

@router.post("/freelancers/{fl_id}/resubmit-verification")
def resubmit_verification(fl_id: int):
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute("SELECT fl_id FROM freelancers WHERE fl_id = %s", (fl_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Freelancer not found")
        cursor.execute(
            "UPDATE fl_verification SET is_latest = FALSE WHERE fl_id = %s",
            (fl_id,)
        )
        cursor.execute(
            """
            INSERT INTO fl_verification (fl_id, fl_verify_status, is_latest, fl_submitted_at)
            VALUES (%s, 'PENDING', TRUE, NOW())
            """,
            (fl_id,)
        )
        cursor.execute(
            "UPDATE freelancers SET fl_verify_status = 'PENDING' WHERE fl_id = %s",
            (fl_id,)
        )
        conn.commit()
        return {"success": True, "fl_verify_status": "PENDING"}
    except HTTPException:
        raise
    except Exception as e:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()

@router.patch("/fl-documents/{doc_id}")
def review_fl_document(doc_id: str, body: DocReviewRequest):
    status_err = validate_doc_review_status(body.status)
    if status_err:
        raise HTTPException(status_code=400, detail=status_err)
    if body.status == "REJECTED" and not (body.reason or "").strip():
        raise HTTPException(status_code=400, detail="Rejection reason is required.")
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute("SELECT fl_doc_id, fl_id FROM fl_documents WHERE fl_doc_id = %s", (doc_id,))
        doc = cursor.fetchone()
        if not doc:
            raise HTTPException(status_code=404, detail="Document not found")

        reject_reason = body.reason if body.status == "REJECTED" else None
        cursor.execute(
            """
            UPDATE fl_documents
            SET fl_doc_status = %s, reviewed_by = %s, reviewed_at = NOW(),
                reject_reason = %s
            WHERE fl_doc_id = %s
            """,
            (body.status, body.reviewed_by, reject_reason, doc_id)
        )

        if body.status == "APPROVED":
            cursor.execute(
                """
                SELECT COUNT(*) AS total,
                  SUM(CASE WHEN fl_doc_status = 'APPROVED' THEN 1 ELSE 0 END) AS approved,
                  SUM(CASE WHEN fl_doc_status = 'PENDING'  THEN 1 ELSE 0 END) AS pending
                FROM fl_documents
                WHERE fl_id = %s AND file_url IS NOT NULL
                """,
                (doc["fl_id"],)
            )
            counts = cursor.fetchone()
            new_status = determine_verify_status(
                counts["total"] or 0,
                counts["approved"] or 0,
                counts["pending"] or 0,
            )
            cursor.execute(
                "UPDATE freelancers SET fl_verify_status = %s WHERE fl_id = %s",
                (new_status, doc["fl_id"])
            )
            if new_status == "VERIFIED":
                cursor.execute(
                    """
                    UPDATE fl_verification SET fl_verify_status = 'VERIFIED',
                    fl_verified_at = NOW(), reviewed_by = %s
                    WHERE fl_id = %s AND is_latest = 1
                    """,
                    (body.reviewed_by, doc["fl_id"])
                )
            else:
                cursor.execute(
                    """
                    UPDATE fl_verification SET fl_verify_status = 'PENDING'
                    WHERE fl_id = %s AND is_latest = 1
                    """,
                    (doc["fl_id"],)
                )
        elif body.status == "REJECTED":
            cursor.execute(
                """
                SELECT
                  SUM(CASE WHEN fl_doc_status = 'REJECTED' THEN 1 ELSE 0 END) AS rejected,
                  SUM(CASE WHEN fl_doc_status = 'PENDING'  THEN 1 ELSE 0 END) AS pending,
                  SUM(CASE WHEN fl_doc_status = 'APPROVED' THEN 1 ELSE 0 END) AS approved,
                  COUNT(*) AS total
                FROM fl_documents
                WHERE fl_id = %s AND file_url IS NOT NULL
                """,
                (doc["fl_id"],)
            )
            counts = cursor.fetchone()
            new_status = determine_verify_status(
                counts["total"] or 0,
                counts["approved"] or 0,
                counts["pending"] or 0,
            )
            all_rejected = new_status == "NOT_VERIFIED"
            cursor.execute(
                "UPDATE freelancers SET fl_verify_status = %s WHERE fl_id = %s",
                (new_status, doc["fl_id"])
            )
            if all_rejected:
                cursor.execute(
                    """
                    UPDATE fl_verification SET fl_verify_status = 'NOT_VERIFIED'
                    WHERE fl_id = %s AND is_latest = 1
                    """,
                    (doc["fl_id"],)
                )
            else:
                cursor.execute(
                    """
                    UPDATE fl_verification SET fl_verify_status = 'PENDING'
                    WHERE fl_id = %s AND is_latest = 1
                    """,
                    (doc["fl_id"],)
                )

        if body.status == "PENDING":
            cursor.execute(
                "UPDATE freelancers SET fl_verify_status = 'PENDING' WHERE fl_id = %s",
                (doc["fl_id"],)
            )
            cursor.execute(
                """
                UPDATE fl_verification SET fl_verify_status = 'PENDING'
                WHERE fl_id = %s AND is_latest = 1
                """,
                (doc["fl_id"],)
            )

        cursor.execute(
            """
            SELECT f.fl_name, fd.fl_doc_type
            FROM fl_documents fd
            JOIN freelancers f ON fd.fl_id = f.fl_id
            WHERE fd.fl_doc_id = %s
            """,
            (doc_id,)
        )
        doc_info = cursor.fetchone()
        if doc_info:
            doc_label = doc_info["fl_doc_type"].replace('_', ' ').title()
            if body.status == 'REJECTED':
                log_note = f"{doc_label}: {body.reason}" if body.reason else doc_label
                cursor.execute(
                    """
                    INSERT INTO admin_logs
                        (admin_id, action_type, target_type, target_id, target_name, note)
                    VALUES (%s, 'REJECT_DOCUMENT', 'DOCUMENT', %s, %s, %s)
                    """,
                    (body.reviewed_by, doc_id, doc_info["fl_name"], log_note)
                )
                if all_rejected:
                    cursor.execute("SELECT fl_name FROM freelancers WHERE fl_id = %s", (doc["fl_id"],))
                    fl_info = cursor.fetchone()
                    cursor.execute(
                        """
                        INSERT INTO admin_logs
                            (admin_id, action_type, target_type, target_id, target_name, note)
                        VALUES (%s, 'NOT_VERIFY_FREELANCER', 'FREELANCER', %s, %s, 'All uploaded documents rejected')
                        """,
                        (body.reviewed_by, doc["fl_id"], fl_info["fl_name"] if fl_info else doc["fl_id"])
                    )
            elif body.status == "APPROVED":
                cursor.execute(
                    """
                    INSERT INTO admin_logs
                        (admin_id, action_type, target_type, target_id, target_name, note)
                    VALUES (%s, 'APPROVE_DOCUMENT', 'DOCUMENT', %s, %s, %s)
                    """,
                    (body.reviewed_by, doc_id, doc_info["fl_name"], doc_label)
                )
                cursor.execute(
                    """
                    SELECT COUNT(*) AS c FROM fl_documents 
                    WHERE fl_id = %s AND fl_doc_status != 'APPROVED' AND file_url IS NOT NULL
                    """,
                    (doc["fl_id"],)
                )
                if cursor.fetchone()["c"] == 0:
                    cursor.execute("SELECT fl_name FROM freelancers WHERE fl_id = %s", (doc["fl_id"],))
                    fl_info = cursor.fetchone()
                    cursor.execute(
                        """
                        INSERT INTO admin_logs
                            (admin_id, action_type, target_type, target_id, target_name, note)
                        VALUES (%s, 'VERIFY_FREELANCER', 'FREELANCER', %s, %s, 'All documents approved')
                        """,
                        (body.reviewed_by, doc["fl_id"], fl_info["fl_name"] if fl_info else doc["fl_id"])
                    )
            elif body.status == "PENDING":
                cursor.execute(
                    """
                    INSERT INTO admin_logs
                        (admin_id, action_type, target_type, target_id, target_name, note)
                    VALUES (%s, 'RESET_DOCUMENT', 'DOCUMENT', %s, %s, %s)
                    """,
                    (body.reviewed_by, doc_id, doc_info["fl_name"], doc_label)
                )

        conn.commit()
        return {"status": "updated", "doc_id": doc_id, "new_status": body.status}
    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR] review_fl_document: {e}")
        if conn:
            conn.rollback()
        return {"error": str(e)}
    finally:
        if conn:
            conn.close()

@router.patch("/freelancers/{fl_id}/ban")
def ban_freelancer(fl_id: str, body: BanRequest):
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute("SELECT fl_id FROM freelancers WHERE fl_id = %s", (fl_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Freelancer not found")
        cursor.execute(
            "UPDATE freelancers SET fl_is_active = %s WHERE fl_id = %s",
            (body.is_active, fl_id)
        )
        cursor.execute("SELECT fl_name FROM freelancers WHERE fl_id = %s", (fl_id,))
        fl_info = cursor.fetchone()
        action = 'UNBAN_USER' if body.is_active else 'BAN_USER'
        cursor.execute(
            """
            INSERT INTO admin_logs
                (admin_id, action_type, target_type, target_id, target_name, note)
            VALUES (%s, %s, 'FREELANCER', %s, %s, NULL)
            """,
            (body.admin_id, action, fl_id, fl_info["fl_name"] if fl_info else fl_id)
        )
        conn.commit()
        return {"status": "updated", "fl_id": fl_id, "is_active": body.is_active}
    except HTTPException:
        raise
    except Exception as e:
        return {"error": str(e)}
    finally:
        if conn:
            conn.close()

@router.get("/languages")
def get_languages():
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute("SELECT language_id, language_name FROM languages ORDER BY language_name ASC")
        return cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()


@router.post("/languages")
def create_or_get_language(data: dict):
    conn = None
    try:
        name, name_err = validate_language_name(data.get("language_name"))
        if name_err:
            raise HTTPException(status_code=400, detail=name_err)
        conn = get_connection()
        cursor = get_cursor(conn)
        # check if exists (case-insensitive)
        cursor.execute(
            "SELECT language_id, language_name FROM languages WHERE LOWER(language_name) = LOWER(%s)",
            (name,)
        )
        existing = cursor.fetchone()
        if existing:
            return existing
        # insert new
        cursor.execute("INSERT INTO languages (language_name) VALUES (%s)", (name,))
        conn.commit()
        return {"language_id": cursor.lastrowid, "language_name": name}
    except HTTPException:
        raise
    except Exception as e:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()