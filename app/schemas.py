from pydantic import BaseModel, EmailStr, ConfigDict

class ClientCreate(BaseModel):
    name: str
    email: EmailStr
    company: str | None = None
    phone: str | None = None


class ClientUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    company: str | None = None
    phone: str | None = None


class ClientResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    company: str | None = None
    phone: str | None = None

    model_config = ConfigDict(from_attributes=True)