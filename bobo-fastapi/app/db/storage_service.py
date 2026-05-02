import uuid
from fastapi import UploadFile
from app.db.supabase_client import supabase, BUCKET_NAME

async def upload_image_to_supabase(file: UploadFile) -> str:
    # Create a unique filename to avoid collisions
    extension = file.filename.split(".")[-1]
    file_path = f"uploads/{uuid.uuid4()}.{extension}"

    # Read the file bytes
    contents = await file.read()

    # Upload to Supabase
    supabase.storage.from_(BUCKET_NAME).upload(
        path=file_path,
        file=contents,
        file_options={"content-type": file.content_type}
    )

    # Get and return the public URL
    public_url = supabase.storage.from_(BUCKET_NAME).get_public_url(file_path)
    
    return public_url