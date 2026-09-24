from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Client, Invoice
from app.schemas import InvoiceCreate, InvoiceResponse, InvoiceStatus


router = APIRouter(
    prefix="/invoices",
    tags=["Invoices"]
)


@router.post("/", response_model=InvoiceResponse, status_code=201)
def create_invoice(
    invoice: InvoiceCreate,
    db: Session = Depends(get_db)
):
    client = db.query(Client).filter(
        Client.id == invoice.client_id
    ).first()

    if not client:
        raise HTTPException(
            status_code=404,
            detail="Client not found"
        )

    new_invoice = Invoice(
        client_id=invoice.client_id,
        service=invoice.service,
        amount=invoice.amount,
        status=invoice.status.value,
        due_date=invoice.due_date
    )

    db.add(new_invoice)
    db.commit()
    db.refresh(new_invoice)

    return new_invoice


@router.get("/", response_model=list[InvoiceResponse])
def get_invoices(
    status: InvoiceStatus | None = None,
    client_id: int | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(Invoice)

    if status:
        query = query.filter(
            Invoice.status == status.value
        )

    if client_id:
        query = query.filter(
            Invoice.client_id == client_id
        )

    return query.all()


@router.get("/{invoice_id}", response_model=InvoiceResponse)
def get_invoice(
    invoice_id: int,
    db: Session = Depends(get_db)
):
    invoice = db.query(Invoice).filter(
        Invoice.id == invoice_id
    ).first()

    if not invoice:
        raise HTTPException(
            status_code=404,
            detail="Invoice not found"
        )

    return invoice

@router.patch("/{invoice_id}/pay", response_model=InvoiceResponse)
def mark_invoice_paid(
    invoice_id: int,
    db: Session = Depends(get_db)
):
    invoice = db.query(Invoice).filter(
        Invoice.id == invoice_id
    ).first()

    if not invoice:
        raise HTTPException(
            status_code=404,
            detail="Invoice not found"
        )

    invoice.status = "paid"
    invoice.paid_at = datetime.utcnow()

    db.commit()
    db.refresh(invoice)

    return invoice