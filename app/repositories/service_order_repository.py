from sqlalchemy.orm import Session, joinedload

from app.models.service_order import ServiceOrder
from app.schemas.service_order import ServiceOrderCreate
from app.utils.enums import ServiceOrderPriority, ServiceOrderStatus

def create_service_order(db: Session,service_order_data: ServiceOrderCreate,) -> ServiceOrder:
    service_order = ServiceOrder(
        title=service_order_data.title,
        description=service_order_data.description,
        priority=service_order_data.priority,
        client_id=service_order_data.client_id,
        responsible_user_id=service_order_data.responsible_user_id,
    )

    db.add(service_order)
    db.commit()
    db.refresh(service_order)

    return get_service_order_by_id(db, service_order.id)

def get_service_orders(
        db: Session, 
        status: ServiceOrderStatus | None = None,
        priority: ServiceOrderPriority | None = None,
        client_id: int | None = None,
        responsible_user_id: int | None = None,
        skip: int = 0,
        limit: int = 10

) -> list[ServiceOrder]:
    query = db.query(ServiceOrder)

    if status is not None:
        query = query.filter(ServiceOrder.status == status)

    if priority is not None:
        query = query.filter(ServiceOrder.priority == priority)

    if client_id is not None:
        query = query.filter(ServiceOrder.client_id == client_id)

    if responsible_user_id is not None:
        query = query.filter(ServiceOrder.responsible_user_id == responsible_user_id)

    return (
        query
        .order_by(ServiceOrder.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_service_order_by_id(db: Session, service_order_id: int) -> ServiceOrder:
    return (
        db.query(ServiceOrder)
        .options(
            joinedload(ServiceOrder.client),
            joinedload(ServiceOrder.responsible_user),
        )
        .filter(ServiceOrder.id == service_order_id)
        .first()
    )

def update_service_order_status(db: Session, service_order: ServiceOrder, new_status: ServiceOrderStatus) -> ServiceOrder:
    service_order.status = new_status
    db.commit()
    db.refresh(service_order)
    return service_order