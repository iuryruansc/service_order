from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.repositories.service_order_history_repository import get_history_by_service_order_id
from app.repositories.service_order_repository import (
    get_service_order_by_id,
    get_service_orders,
)
from app.schemas.service_order import ServiceOrderCreate, ServiceOrderRead, ServiceOrderStatusUpdate
from app.schemas.service_order_history import ServiceOrderHistoryRead
from app.services.service_order_service import change_service_order_status, register_service_order
from app.utils.enums import ServiceOrderPriority, ServiceOrderStatus

router = APIRouter(prefix="/service-orders", tags=["service-orders"])

@router.post("/", response_model=ServiceOrderRead, status_code=status.HTTP_201_CREATED)
def create_service_order(
    service_order_data: ServiceOrderCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    try:
        return register_service_order(db, service_order_data)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=str(error)
        ) from error
    

@router.get("/", response_model=list[ServiceOrderRead])
def list_service_orders(
    status: ServiceOrderStatus | None = None,
    priority: ServiceOrderPriority | None = None,
    client_id: int | None = None,
    responsible_user_id: int | None = None,
    db: Session = Depends(get_db),
    _authenticated_user=Depends(get_current_user)
):
    return get_service_orders(
        db=db,
        status=status,
        priority=priority,
        client_id=client_id,
        responsible_user_id=responsible_user_id
    )

@router.get("/{service_order_id}", response_model=ServiceOrderRead)
def get_service_order(
    service_order_id: int,
    db: Session = Depends(get_db),
    _authenticated_user=Depends(get_current_user)
):
    service_order = get_service_order_by_id(db, service_order_id)

    if not service_order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Service order not found with the provided ID"
        )

    return service_order

@router.patch("/{service_order_id}/status", response_model=ServiceOrderRead)
def update_service_order_status(
    service_order_id: int,
    status_update: ServiceOrderStatusUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    try:
        return change_service_order_status(
            db=db, 
            service_order_id=service_order_id, 
            new_status=status_update.status, 
            current_user_id=current_user.id, 
            note=status_update.note,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=str(error)
        ) from error
    
@router.get("/{service_order_id}/history", response_model=list[ServiceOrderHistoryRead])
def get_service_order_history(
    service_order_id: int,
    db: Session = Depends(get_db), 
    _authenticated_user=Depends(get_current_user)
):
    service_order = get_service_order_by_id(db, service_order_id)

    if not service_order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Service order not found with the provided ID"
        )

    return get_history_by_service_order_id(db, service_order_id)