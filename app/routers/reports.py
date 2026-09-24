from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Invoice


router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)


@router.get("/summary")
def get_summary(
    db: Session = Depends(get_db)
):
    total_invoices = db.query(
        func.count(Invoice.id)
    ).scalar()

    total_income = db.query(
        func.coalesce(func.sum(Invoice.amount), 0)
    ).filter(
        Invoice.status == "paid"
    ).scalar()

    unpaid_total = db.query(
        func.coalesce(func.sum(Invoice.amount), 0)
    ).filter(
        Invoice.status == "unpaid"
    ).scalar()

    return {
        "total_invoices": total_invoices,
        "total_income": float(total_income),
        "unpaid_total": float(unpaid_total)
    }