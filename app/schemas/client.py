from pydantic import BaseModel, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber

class ClientBase(BaseModel):
    name: str
    email: EmailStr
    phone: PhoneNumber | None = None

class ClientCreate(ClientBase):
    pass

class ClientRead(ClientBase):
    id: int
    is_active: bool

    model_config = {
        "from_attributes": True
    }