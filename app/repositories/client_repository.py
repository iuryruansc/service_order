from typing import List

from sqlalchemy.orm import Session 

from app.models.client import Client
from app.schemas.client import ClientCreate

def get_client_by_email(db: Session, email: str):
    return db.query(Client).filter(Client.email == email).first()

def create_client(db: Session, client_data: ClientCreate):
    client = Client(
        name=client_data.name,
        email=client_data.email,
        phone=client_data.phone,
    )

    db.add(client)
    db.commit()
    db.refresh(client)

    return client

def get_clients(db: Session) -> List[Client]:
    return db.query(Client).all()