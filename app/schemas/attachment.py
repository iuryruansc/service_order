from datetime import datetime

from pydantic import BaseModel

class AttachmentBase(BaseModel):
    filename: str

class AttachmentCreate(AttachmentBase):
    service_order_id: int
    uploaded_by_id: int
    file_path: str

class AttachmentRead(AttachmentBase):
    id: int
    service_order_id: int
    uploaded_by_id: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }