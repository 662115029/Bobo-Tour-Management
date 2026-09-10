import uuid
from fastapi import UploadFile
from app.db.supabase_client import supabase, BUCKET_NAME


async def upload_image_to_supabase(file: UploadFile, folder: str = "uploads") -> str:
    extension = file.filename.split(".")[-1]
    file_path = f"{folder}/{uuid.uuid4()}.{extension}"

    contents = await file.read()

    supabase.storage.from_(BUCKET_NAME).upload(
        path=file_path,
        file=contents,
        file_options={"content-type": file.content_type}
    )

    public_url = supabase.storage.from_(BUCKET_NAME).get_public_url(file_path)

    return public_url



# import uuid
# from fastapi import UploadFile
# from app.db.supabase_client import supabase, BUCKET_NAME

# # TEMP — remove after STC-14-TD-05
# SIMULATE_UPLOAD_FAILURE = True


# async def upload_image_to_supabase(file: UploadFile, folder: str = "uploads") -> str:
#     extension = file.filename.split(".")[-1]
#     file_path = f"{folder}/{uuid.uuid4()}.{extension}"

#     contents = await file.read()

#     if SIMULATE_UPLOAD_FAILURE:  # TEMP — remove after STC-14-TD-05
#         raise Exception("Failed to upload document. Please try again.")

#     supabase.storage.from_(BUCKET_NAME).upload(
#         path=file_path,
#         file=contents,
#         file_options={"content-type": file.content_type}
#     )

#     public_url = supabase.storage.from_(BUCKET_NAME).get_public_url(file_path)

#     return public_url