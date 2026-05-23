from sqlalchemy import func
from sqlalchemy.orm import Session


from app.models.service_order import ServiceOrder
from app.utils.enums import ServiceOrderPriority, ServiceOrderStatus

def get_orders_count_by_status(db: Session) -> dict:
    results = (
        db.query(ServiceOrder.status, func.count(ServiceOrder.id))
        .group_by(ServiceOrder.status)
        .all()
    )

    counts = {status: 0 for status in ServiceOrderStatus}
    for status, count in results:
        counts[status] = count

    return counts

def get_orders_count_by_priority(db: Session) -> dict:
    results = (
        db.query(ServiceOrder.priority, func.count(ServiceOrder.id))
        .group_by(ServiceOrder.priority)
        .all()
    )

    counts = {priority: 0 for priority in ServiceOrderPriority}
    for priority, count in results:
        counts[priority] = count

    return counts

def get_total_orders(db: Session) -> int:
    return db.query(func.count(ServiceOrder.id)).scalar()
