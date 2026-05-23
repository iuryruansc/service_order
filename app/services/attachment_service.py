import os
import uuid
from fastapi import UploadFile
from sqlalchemy.orm import Session
from app.repositories.attachment_repository import create_attachment, get_attachment_by_id, delete_attachment
from app.repositories.service_order_repository import get_service_order_by_id
from app.schemas.attachment import AttachmentCreate
from app.utils.exceptions import BusinessRuleError, NotFoundError

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".pdf"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

async def upload_attachment(
    db: Session,
    file: UploadFile,
    service_order_id: int,
    uploaded_by_id: int,
):
    service_order = get_service_order_by_id(db, service_order_id)
    if not service_order:
        raise NotFoundError("Service order not found")

    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise BusinessRuleError(f"File type not allowed. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}")

    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise BusinessRuleError("File too large. Maximum size is 5MB")

    os.makedirs("uploads", exist_ok=True)
    file_path = f"uploads/{uuid.uuid4().hex}{ext}"
    with open(file_path, "wb") as f:
        f.write(content)

    attachment_data = AttachmentCreate(
        service_order_id=service_order_id,
        filename=file.filename,
        file_path=file_path,
        uploaded_by_id=uploaded_by_id,
    )

    return create_attachment(db, attachment_data)

async def remove_attachment(db: Session, attachment_id: int):
    attachment = get_attachment_by_id(db, attachment_id)
    if not attachment:
        raise NotFoundError("Attachment not found")

    if os.path.exists(attachment.file_path):
        os.remove(attachment.file_path)

    delete_attachment(db, attachment)