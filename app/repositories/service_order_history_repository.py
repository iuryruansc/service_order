from sqlalchemy.orm import Session

from app.models.service_order_history import ServiceOrderHistory
from app.utils.enums import ServiceOrderStatus

def create_service_order_history(
    db: Session,
    service_order_id: int,
    user_id: int,
    old_status: ServiceOrderStatus,
    new_status: ServiceOrderStatus,
    note: str | None = None,
) -> ServiceOrderHistory:
    history = ServiceOrderHistory(
        service_order_id=service_order_id,
        user_id=user_id,
        old_status=old_status,
        new_status=new_status,
        note=note,
    )

    db.add(history)
    db.commit()
    db.refresh(history)

    return history

def get_history_by_service_order_id(
    db: Session,
    service_order_id: int,
) -> list[ServiceOrderHistory]:
    return (
        db.query(ServiceOrderHistory)
        .filter(ServiceOrderHistory.service_order_id == service_order_id)
        .order_by(ServiceOrderHistory.created_at.desc())
        .all()
    )