from pydantic import BaseModel

class ServiceOrderByStatus(BaseModel):
    open: int
    in_progress: int
    waiting: int
    done: int
    canceled: int

    model_config = {
        "from_attributes": True
    }

class ServiceOrderByPriority(BaseModel):
    low: int
    medium: int
    high: int
    urgent: int

    model_config = {
        "from_attributes": True
    }

class DashboardRead(BaseModel):
    total_service_orders: int
    by_status: ServiceOrderByStatus
    by_priority: ServiceOrderByPriority

    model_config = {
        "from_attributes": True
    }