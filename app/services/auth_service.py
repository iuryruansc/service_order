from sqlalchemy.orm import Session

from app.core.security import verify_password
from app.repositories.user_repository import get_user_by_email
from app.schemas.auth import LoginRequest

def authenticate_user(db: Session, login_data: LoginRequest):
    user = get_user_by_email(db, login_data.email)

    if not user:
        raise ValueError("Invalid credentials")
    
    if not verify_password(login_data.password, user.hashed_password):
        raise ValueError("Invalid credentials")
    
    if not user.is_active:
        raise ValueError("Inactive user")
    
    return user