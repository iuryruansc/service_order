from datetime import datetime

from pydantic import BaseModel

from app.utils.enums import ServiceOrderStatus

class ServiceOrderHistoryRead(BaseModel):
    id: int
    service_order_id: int
    user_id: int
    old_status: ServiceOrderStatus
    new_status: ServiceOrderStatus
    note: str | None = None
    created_at: datetime

    model_config = {
        "from_attributes": True
    }