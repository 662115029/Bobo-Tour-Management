from fastapi import APIRouter, HTTPException, UploadFile, File
from app.db.connection import get_connection, get_cursor
from app.db.storage_service import upload_image_to_supabase
import uuid

router = APIRouter(tags=["uploads"])

ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp"}


@router.post("/upload/image")
async def upload_image(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="Invalid file type. Only JPEG, PNG, and WebP allowed.")
    try:
        url = await upload_image_to_supabase(file)
        return {"url": url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/fl-vehicle/{vehicle_id}/images")
async def upload_vehicle_image(vehicle_id: str, file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="Invalid file type. Only JPEG, PNG, and WebP allowed.")
    try:
        conn = get_connection()
        cursor = get_cursor(conn)

        cursor.execute("SELECT fl_vehicle_id FROM fl_vehicle WHERE fl_vehicle_id = %s", (vehicle_id,))
        if not cursor.fetchone():
            conn.close()
            raise HTTPException(status_code=404, detail="Vehicle not found")

        image_url = await upload_image_to_supabase(file)

        cursor.execute(
            """
            INSERT INTO fl_vehicle_images (fl_vehicle_id, fl_vehicle_image_url)
            VALUES (%s, %s)
            """,
            (vehicle_id, image_url)
        )
        conn.commit()
        new_id = cursor.lastrowid
        conn.close()

        return {
            "fl_vehicle_image_id": new_id,
            "fl_vehicle_id": vehicle_id,
            "fl_vehicle_image_url": image_url
        }
    except HTTPException:
        raise
    except Exception as e:
        return {"error": str(e)}


@router.post("/fl-documents/{fl_id}/upload")
async def upload_fl_document(
    fl_id: str,
    doc_type: str,
    file: UploadFile = File(...),
    vehicle_id: str = None
):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="Invalid file type. Only JPEG, PNG, and WebP allowed.")

    valid_doc_types = {"PERSONAL_ID", "DRIVER_LICENSE", "PUBLIC_DRIVER_LICENSE", "VEHICLE_REGISTRATION", "VEHICLE_INSPECTION"}
    if doc_type not in valid_doc_types:
        raise HTTPException(status_code=400, detail=f"Invalid doc_type. Must be one of: {valid_doc_types}")

    try:
        conn = get_connection()
        cursor = get_cursor(conn)

        cursor.execute("SELECT fl_id FROM freelancers WHERE fl_id = %s", (fl_id,))
        if not cursor.fetchone():
            conn.close()
            raise HTTPException(status_code=404, detail="Freelancer not found")

        image_url = await upload_image_to_supabase(file)

        cursor.execute(
            """
            UPDATE fl_documents
            SET is_latest = 0
            WHERE fl_id = %s AND fl_doc_type = %s AND is_latest = 1
            """,
            (fl_id, doc_type)
        )

        new_doc_id = str(uuid.uuid4())
        cursor.execute(
            """
            INSERT INTO fl_documents 
                (fl_doc_id, fl_id, fl_vehicle_id, fl_doc_type, file_url, fl_doc_status, is_latest)
            VALUES (%s, %s, %s, %s, %s, 'PENDING', 1)
            """,
            (new_doc_id, fl_id, vehicle_id, doc_type, image_url)
        )

        conn.commit()
        conn.close()

        return {
            "fl_doc_id": new_doc_id,
            "fl_id": fl_id,
            "fl_doc_type": doc_type,
            "file_url": image_url,
            "fl_doc_status": "PENDING"
        }
    except HTTPException:
        raise
    except Exception as e:
        return {"error": str(e)}


@router.post("/em-documents/{em_id}/upload")
async def upload_em_document(
    em_id: str,
    doc_type: str,
    file: UploadFile = File(...)
):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="Invalid file type. Only JPEG, PNG, and WebP allowed.")

    valid_doc_types = {"COMPANY_REGISTRATION", "BUSINESS_LICENSE", "TOURISM_LICENSE", "TAX_ID_DOCUMENT", "AUTHORIZED_PERSON_ID"}
    if doc_type not in valid_doc_types:
        raise HTTPException(status_code=400, detail=f"Invalid doc_type. Must be one of: {valid_doc_types}")

    try:
        conn = get_connection()
        cursor = get_cursor(conn)

        cursor.execute("SELECT em_id FROM employers WHERE em_id = %s", (em_id,))
        if not cursor.fetchone():
            conn.close()
            raise HTTPException(status_code=404, detail="Employer not found")

        image_url = await upload_image_to_supabase(file)

        cursor.execute(
            """
            UPDATE em_documents
            SET is_latest = 0
            WHERE em_id = %s AND em_doc_type = %s AND is_latest = 1
            """,
            (em_id, doc_type)
        )

        new_doc_id = str(uuid.uuid4())
        cursor.execute(
            """
            INSERT INTO em_documents
                (em_doc_id, em_id, em_doc_type, file_url, em_doc_status, is_latest)
            VALUES (%s, %s, %s, %s, 'PENDING', 1)
            """,
            (new_doc_id, em_id, doc_type, image_url)
        )

        conn.commit()
        conn.close()

        return {
            "em_doc_id": new_doc_id,
            "em_id": em_id,
            "em_doc_type": doc_type,
            "file_url": image_url,
            "em_doc_status": "PENDING"
        }
    except HTTPException:
        raise
    except Exception as e:
        return {"error": str(e)}