from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_current_admin, get_db
from app.repositories.attachment_repository import get_attachments_by_service_order
from app.schemas.attachment import AttachmentRead
from app.services.attachment_service import upload_attachment, remove_attachment
from app.utils.exceptions import NotFoundError, BusinessRuleError

router = APIRouter(prefix="/service-orders", tags=["attachments"])

@router.post("/{service_order_id}/attachments", response_model=AttachmentRead, status_code=status.HTTP_201_CREATED)
async def upload_attachment_endpoint(
    service_order_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        return await upload_attachment(db, file, service_order_id, current_user.id)
    except NotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))
    except BusinessRuleError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))

@router.get("/{service_order_id}/attachments", response_model=list[AttachmentRead])
def list_attachments(
    service_order_id: int,
    db: Session = Depends(get_db),
    _current_user=Depends(get_current_user),
):
    return get_attachments_by_service_order(db, service_order_id)

@router.delete("/{service_order_id}/attachments/{attachment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_attachment_endpoint(
    service_order_id: int,
    attachment_id: int,
    db: Session = Depends(get_db),
    _current_admin=Depends(get_current_admin),
):
    try:
        await remove_attachment(db, attachment_id)
    except NotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))