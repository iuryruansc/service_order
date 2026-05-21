from typing import List

from sqlalchemy.orm import Session

from app.models.service_order import ServiceOrder
from app.schemas.service_order import ServiceOrderCreate
from app.utils.enums import ServiceOrderStatus

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

    return service_order

def get_service_orders(db: Session) -> List[ServiceOrder]:
    return db.query(ServiceOrder).all()

def get_service_order_by_id(db: Session, service_order_id: int) -> ServiceOrder:
    return db.query(ServiceOrder).filter(ServiceOrder.id == service_order_id).first()

def update_service_order_status(db: Session, service_order: ServiceOrder, new_status: ServiceOrderStatus) -> ServiceOrder:
    service_order.status = new_status
    db.commit()
    db.refresh(service_order)
    return service_order