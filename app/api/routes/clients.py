from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.schemas.client import ClientCreate, ClientRead
from app.services.client_service import register_client
from app.repositories.client_repository import get_clients

router = APIRouter(prefix="/clients", tags=["clients"])

@router.post("/", response_model=ClientRead, status_code=status.HTTP_201_CREATED)
def create_client(client_data: ClientCreate, db: Session = Depends(get_db), _current_user = Depends(get_current_user)):
    try:
        return register_client(db, client_data)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        ) from error
    
@router.get("/", response_model=list[ClientRead])
def list_clients(db: Session = Depends(get_db), _current_user = Depends(get_current_user)):
    return get_clients(db)