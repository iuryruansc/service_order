from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_admin, get_db
from app.schemas.user import UserCreate, UserRead
from app.services.user_service import register_user, activate_user, deactivate_user
from app.repositories.user_repository import get_users, get_user_by_id
from app.utils.exceptions import BusinessRuleError, NotFoundError

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    try:
        return register_user(db, user_data)
    except BusinessRuleError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        ) from error
    
@router.get("/", response_model=list[UserRead])
def list_users(db: Session = Depends(get_db), _authenticated_admin=Depends(get_current_admin)):
    return get_users(db)

@router.patch("/{user_id}/activate", response_model=UserRead)
def activate_user_endpoint(user_id: int, db: Session = Depends(get_db), _authenticated_admin=Depends(get_current_admin)):
    try:
        return activate_user(db, user_id)
    except NotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        ) from error

@router.patch("/{user_id}/deactivate", response_model=UserRead)
def deactivate_user_endpoint(user_id: int, db: Session = Depends(get_db), _authenticated_admin=Depends(get_current_admin)):
    try:
        return deactivate_user(db, user_id)
    except NotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        ) from error