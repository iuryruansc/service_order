from sqlalchemy.orm import Session 

from app.models.attachment import Attachment
from app.schemas.attachment import AttachmentCreate

def create_attachment(db: Session, attachment_data: AttachmentCreate) -> Attachment:
    attachment = Attachment(
        service_order_id = attachment_data.service_order_id,
        filename = attachment_data.filename,
        file_path = attachment_data.file_path,
        uploaded_by_id = attachment_data.uploaded_by_id,
    )

    db.add(attachment)
    db.commit()
    db.refresh(attachment)

    return attachment

def get_attachments_by_service_order(db: Session, service_order_id: int) -> list[Attachment]:
    return db.query(Attachment).filter(Attachment.service_order_id == service_order_id).all()

def get_attachment_by_id(db: Session, attachment_id: int) -> Attachment:
    return db.query(Attachment).filter(Attachment.id == attachment_id).first()

def delete_attachment(db: Session, attachment: Attachment) -> None:
    db.delete(attachment)
    db.commit()