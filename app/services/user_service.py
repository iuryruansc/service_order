from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.repositories.user_repository import activate_user_repo, deactivate_user_repo, get_user_by_email, create_user, get_user_by_id
from app.schemas.user import UserCreate
from app.utils.exceptions import BusinessRuleError, NotFoundError

def register_user(db: Session, user_data: UserCreate):
    existing_user = get_user_by_email(db, user_data.email)

    if existing_user:
        raise BusinessRuleError("Email already registered")
    
    hashed_password = get_password_hash(user_data.password)

    return create_user(
        db=db,
        user_data=user_data,
        hashed_password=hashed_password
    )

def activate_user(db: Session, user_id: int):
    user = get_user_by_id(db, user_id)

    if not user:
        raise NotFoundError("User not found")
    
    return activate_user_repo(db, user)

def deactivate_user(db: Session, user_id: int):
    user = get_user_by_id(db, user_id)

    if not user:
        raise NotFoundError("User not found")
    
    return deactivate_user_repo(db, user)