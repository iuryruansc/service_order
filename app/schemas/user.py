from pydantic import BaseModel, EmailStr

from app.utils.enums import UserRole

class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int
    is_active: bool
    role: UserRole

    model_config = {
        "from_attributes": True
    }