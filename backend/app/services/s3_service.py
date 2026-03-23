from uuid import uuid4

from app.core.config import get_settings


def _get_s3_client():
    import boto3

    settings = get_settings()

    return boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION,
    )


def upload_file(file, folder: str) -> str:
    settings = get_settings()
    extension = ""
    if getattr(file, "filename", None) and "." in file.filename:
        extension = f".{file.filename.rsplit('.', 1)[1]}"

    filename = f"{uuid4()}{extension}"
    key = f"{folder}/{filename}"

    _get_s3_client().upload_fileobj(
        file.file,
        settings.AWS_BUCKET_NAME,
        key,
        ExtraArgs={"ContentType": file.content_type},
    )

    return f"https://{settings.AWS_BUCKET_NAME}.s3.{settings.AWS_REGION}.amazonaws.com/{key}"
