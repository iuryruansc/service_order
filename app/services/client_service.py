from sqlalchemy.orm import Session

from app.repositories.client_repository import get_client_by_email, create_client
from app.schemas.client import ClientCreate

def register_client(db: Session, client_data: ClientCreate):
    existing_client = get_client_by_email(db, client_data.email)

    if existing_client:
        raise ValueError("Email already registered")
    
    return create_client(
        db=db, 
        client_data=client_data
    )
