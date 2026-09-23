from datetime import date, datetime
from decimal import Decimal
from enum import Enum

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

class InvoiceStatus(str, Enum):
    unpaid = "unpaid"
    paid = "paid"
    overdue = "overdue"


class InvoiceCreate(BaseModel):
    client_id: int
    service: str
    amount: Decimal
    status: InvoiceStatus = InvoiceStatus.unpaid
    due_date: date


class InvoiceResponse(BaseModel):
    id: int
    client_id: int
    service: str
    amount: Decimal
    status: InvoiceStatus
    due_date: date
    created_at: datetime
    paid_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)