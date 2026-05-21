from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.repositories.user_repository import get_user_by_email, create_user
from app.schemas.user import UserCreate

def register_user(db: Session, user_data: UserCreate):
    existing_user = get_user_by_email(db, user_data.email)

    if existing_user:
        raise ValueError("Email already registered")
    
    hashed_password = get_password_hash(user_data.password)

    return create_user(
        db=db,
        user_data=user_data,
        hashed_password=hashed_password
    )
