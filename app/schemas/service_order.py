from datetime import datetime

from pydantic import BaseModel

from app.utils.enums import ServiceOrderPriority, ServiceOrderStatus

class ServiceOrderBase(BaseModel):
    title: str
    description: str
    priority: ServiceOrderPriority = ServiceOrderPriority.MEDIUM

class ServiceOrderCreate(ServiceOrderBase):
    client_id: int
    responsible_user_id: int

class ServiceOrderRead(ServiceOrderBase):
    id: int
    status: ServiceOrderStatus
    client_id: int
    responsible_user_id: int
    created_at: datetime
    updated_at: datetime
    is_active: bool

    model_config = {
        "from_attributes": True
    }

class ServiceOrderStatusUpdate(BaseModel):
    status: ServiceOrderStatus
    note: str | None = None