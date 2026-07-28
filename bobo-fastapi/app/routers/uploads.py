from fastapi import APIRouter, HTTPException, UploadFile, File
from app.db.connection import get_connection, get_cursor
from app.db.storage_service import upload_image_to_supabase

router = APIRouter(tags=["uploads"])

ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp"}
ALLOWED_TYPES_WITH_PDF = {"image/jpeg", "image/png", "image/webp", "application/pdf"}
ALLOWED_DOC_TYPES = {"image/jpeg", "image/png", "application/pdf"}
DOC_TYPE_ERROR = "File must be in .jpg, .png, or .pdf format only."


@router.post("/upload/image")
async def upload_image(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="Invalid file type.")
    try:
        url = await upload_image_to_supabase(file, folder="uploads/profiles/employers")
        return {"url": url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/upload/employer-profile")
async def upload_employer_profile(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="Invalid file type.")
    try:
        url = await upload_image_to_supabase(file, folder="uploads/profiles/employers")
        return {"url": url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/upload/freelancer-profile")
async def upload_freelancer_profile(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="Invalid file type.")
    try:
        url = await upload_image_to_supabase(file, folder="uploads/profiles/freelancers")
        return {"url": url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/upload/payment-slip")
async def upload_payment_slip(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="Invalid file type.")
    try:
        url = await upload_image_to_supabase(file, folder="uploads/payment")
        return {"url": url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/fl-vehicle/{vehicle_id}/images")
async def upload_vehicle_image(vehicle_id: str, file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="Invalid file type.")
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute("SELECT fl_vehicle_id FROM fl_vehicle WHERE fl_vehicle_id = %s", (vehicle_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Vehicle not found")
        image_url = await upload_image_to_supabase(file, folder="uploads/vehicles")
        cursor.execute(
            "INSERT INTO fl_vehicle_images (fl_vehicle_id, fl_vehicle_image_url) VALUES (%s, %s)",
            (vehicle_id, image_url)
        )
        conn.commit()
        return {"fl_vehicle_image_id": cursor.lastrowid, "fl_vehicle_id": vehicle_id, "fl_vehicle_image_url": image_url}
    except HTTPException:
        raise
    except Exception as e:
        return {"error": str(e)}
    finally:
        if conn:
            conn.close()


@router.post("/fl-documents/{fl_id}/upload")
async def upload_fl_document(fl_id: str, doc_type: str, file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_DOC_TYPES:
       raise HTTPException(status_code=400, detail=DOC_TYPE_ERROR)
    contents = await file.read()
    if len(contents) > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File size must not exceed 5 MB.")
    await file.seek(0)
    valid_doc_types = {"PERSONAL_ID", "DRIVER_LICENSE", "PUBLIC_DRIVER_LICENSE", "VEHICLE_REGISTRATION", "VEHICLE_INSPECTION"}
    if doc_type not in valid_doc_types:
        raise HTTPException(status_code=400, detail=f"Invalid doc_type.")
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute("SELECT fl_id FROM freelancers WHERE fl_id = %s", (fl_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Freelancer not found")
        image_url = await upload_image_to_supabase(file, folder="uploads/documents/freelancers")
        cursor.execute(
            """
            UPDATE fl_documents
            SET file_url = %s, fl_doc_status = 'PENDING', fl_uploaded_at = NOW(), reject_reason = NULL
            WHERE fl_id = %s AND fl_doc_type = %s
            """,
            (image_url, fl_id, doc_type)
        )
        conn.commit()
        return {"fl_id": fl_id, "fl_doc_type": doc_type, "file_url": image_url, "fl_doc_status": "PENDING"}
    except HTTPException:
        raise
    except Exception as e:
        return {"error": str(e)}
    finally:
        if conn:
            conn.close()


@router.post("/em-documents/{em_id}/upload")
async def upload_em_document(em_id: str, doc_type: str, file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_DOC_TYPES:
       raise HTTPException(status_code=400, detail=DOC_TYPE_ERROR)
    contents = await file.read()
    if len(contents) > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File must not exceed 5 MB size.")
    await file.seek(0)
    valid_doc_types = {"COMPANY_REGISTRATION", "BUSINESS_LICENSE", "TOURISM_LICENSE", "TAX_ID_DOCUMENT", "AUTHORIZED_PERSON_ID"}
    if doc_type not in valid_doc_types:
        raise HTTPException(status_code=400, detail=f"Invalid doc_type.")
    conn = None
    try:
        conn = get_connection()
        cursor = get_cursor(conn)
        cursor.execute("SELECT em_id FROM employers WHERE em_id = %s", (em_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Employer not found")
        image_url = await upload_image_to_supabase(file, folder="uploads/documents/employers")
        cursor.execute(
            """
            INSERT INTO em_documents (em_id, em_doc_type, file_url, em_doc_status, em_uploaded_at, reject_reason)
            VALUES (%s, %s, %s, 'PENDING', NOW(), NULL)
            ON DUPLICATE KEY UPDATE
                file_url = VALUES(file_url),
                em_doc_status = 'PENDING',
                em_uploaded_at = NOW(),
                reject_reason = NULL
            """,
            (em_id, doc_type, image_url)
        )
        conn.commit()
        return {"em_id": em_id, "em_doc_type": doc_type, "file_url": image_url, "em_doc_status": "PENDING"}
    except HTTPException:
        raise
    except Exception as e:
        return {"error": str(e)}
    finally:
        if conn:
            conn.close()