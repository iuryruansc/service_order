from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from fastapi.responses import StreamingResponse

from app.api.deps import get_current_user, get_db, get_current_admin
from app.repositories.service_order_history_repository import get_history_by_service_order_id
from app.repositories.service_order_repository import (
    get_service_order_by_id,
    get_service_orders,
)
from app.schemas.service_order import ServiceOrderCreate, ServiceOrderRead, ServiceOrderStatusUpdate
from app.schemas.service_order_history import ServiceOrderHistoryRead
from app.services.service_order_service import change_service_order_status, register_service_order
from app.services.export_service import export_to_excel, export_to_pdf
from app.services.email_service import send_order_created_email, send_status_changed_email, send_order_canceled_email
from app.utils.enums import ServiceOrderPriority, ServiceOrderStatus, ExportFormat
from app.utils.exceptions import BusinessRuleError, NotFoundError

router = APIRouter(prefix="/service-orders", tags=["service-orders"])

@router.post("/", response_model=ServiceOrderRead, status_code=status.HTTP_201_CREATED)
async def create_service_order(
    service_order_data: ServiceOrderCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    try:
        order = register_service_order(db, service_order_data)

        await send_order_created_email(
            responsible_email=order.responsible_user.email,
            responsible_name=order.responsible_user.name,
            order_title=order.title,
            order_id=order.id,
        )

        return order
    except NotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=str(error)
        ) from error
    except BusinessRuleError as error:
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
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db),
    _authenticated_user=Depends(get_current_user)
):
    return get_service_orders(
        db=db,
        status=status,
        priority=priority,
        client_id=client_id,
        responsible_user_id=responsible_user_id,
        skip=skip,
        limit=limit
    ) 

@router.patch("/{service_order_id}/status", response_model=ServiceOrderRead)
async def update_service_order_status(
    service_order_id: int,
    status_update: ServiceOrderStatusUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    try:
        old_order = get_service_order_by_id(db, service_order_id)
        old_status = old_order.status
        order = change_service_order_status(
            db=db, 
            service_order_id=service_order_id, 
            new_status=status_update.status, 
            current_user_id=current_user.id, 
            note=status_update.note,
        )

        if order.status == ServiceOrderStatus.CANCELED:
            await send_order_canceled_email(
                client_email=order.client.email,
                client_name=order.client.name,
                order_title=order.title,
                order_id=order.id,
            )
        else:
            await send_status_changed_email(
                responsible_email=current_user.email,
                responsible_name=current_user.name,
                order_title=order.title,
                order_id=order.id,
                old_status=old_status,
                new_status=status_update.status 
            )

        return order
    except NotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=str(error)
        ) from error
    except BusinessRuleError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=str(error)
        ) from error

@router.get("/export")
def export_service_orders(
    format: ExportFormat,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin),
):
    if format == ExportFormat.EXCEL:
        file_content = export_to_excel(db, exported_by=current_user.email)
        return StreamingResponse(
            file_content,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": "attachment; filename=orders.xlsx"},
        )
    
    file_content = export_to_pdf(db, exported_by=current_user.email)
    return StreamingResponse(
        file_content,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=orders.pdf"}
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
    except NotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=str(error)
        ) from error
    except BusinessRuleError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
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
