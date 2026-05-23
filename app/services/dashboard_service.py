from sqlalchemy.orm import Session

from app.repositories.dashboard_repository import (
    get_total_orders,
    get_orders_count_by_status,
    get_orders_count_by_priority,
)

def get_dashboard_data(db: Session):
    return {
        "total_service_orders": get_total_orders(db),
        "by_status": get_orders_count_by_status(db),
        "by_priority": get_orders_count_by_priority(db),
    }