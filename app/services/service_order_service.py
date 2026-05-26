from sqlalchemy.orm import Session

from app.repositories.service_order_history_repository import create_service_order_history
from app.repositories.service_order_repository import create_service_order, get_service_order_by_id, update_service_order_status
from app.repositories.client_repository import get_client_by_id
from app.repositories.user_repository import get_user_by_id
from app.schemas.service_order import ServiceOrderCreate
from app.utils.enums import ServiceOrderStatus
from app.utils.exceptions import NotFoundError, BusinessRuleError

ALLOWED_STATUS_TRANSITIONS = {
    ServiceOrderStatus.OPEN: {
        ServiceOrderStatus.IN_PROGRESS,
        ServiceOrderStatus.CANCELED,
    },
    ServiceOrderStatus.IN_PROGRESS: {
        ServiceOrderStatus.WAITING,
        ServiceOrderStatus.DONE,
        ServiceOrderStatus.CANCELED,
    },
    ServiceOrderStatus.WAITING: {
        ServiceOrderStatus.IN_PROGRESS,
        ServiceOrderStatus.CANCELED,
    },
    ServiceOrderStatus.DONE: set(),
    ServiceOrderStatus.CANCELED: set(),
}

def register_service_order(db: Session, service_order_data: ServiceOrderCreate, responsible_user_id: int):
    client = get_client_by_id(db, service_order_data.client_id)

    if not client:
        raise NotFoundError("Client not found with the provided ID")
    
    responsible_user = get_user_by_id(db, responsible_user_id)

    if not responsible_user:
        raise NotFoundError("Responsible user not found with the provided ID")

    return create_service_order(
        db=db, 
        service_order_data=service_order_data,
        responsible_user_id=responsible_user_id
    )

def change_service_order_status(db: Session, service_order_id: int, new_status: ServiceOrderStatus, current_user_id: int, note: str | None = None):
    service_order = get_service_order_by_id(db, service_order_id)

    if not service_order:
        raise NotFoundError("Service order not found with the provided ID")
    
    validate_status_transition(service_order.status, new_status)

    create_service_order_history(
        db=db,
        service_order_id=service_order_id,
        user_id=current_user_id,
        old_status=service_order.status,
        new_status=new_status,
        note=note,
    )

    return update_service_order_status(db, service_order, new_status)

def validate_status_transition(
    current_status: ServiceOrderStatus,
    new_status: ServiceOrderStatus,
) -> None:
    if new_status == current_status:
        raise BusinessRuleError("Service order already has this status")

    if new_status not in ALLOWED_STATUS_TRANSITIONS.get(current_status, set()):
        raise BusinessRuleError("Invalid status transition")