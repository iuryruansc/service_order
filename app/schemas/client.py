from pydantic import BaseModel, EmailStr, field_validator
import re

class ClientBase(BaseModel):
    name: str
    email: EmailStr
    phone: str | None = None

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value):
        if value is None:
            return value
        
        digits = re.sub(r"\D", "", value)
        
        if len(digits) < 10 or len(digits) > 13:
            raise ValueError("Invalid phone number")
        
        return value

class ClientCreate(ClientBase):
    pass

class ClientRead(ClientBase):
    id: int
    is_active: bool

    model_config = {
        "from_attributes": True
    }