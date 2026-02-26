import datetime
from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.db.connectdb import get_db
from src.models.models import Products, Sales
from src.schemas.stock_schemas import StockReport
from src.schemas.sale_schemas import SaleSummary


router = APIRouter(prefix="/reports", tags=["Relatórios"])

@router.get("/stock", response_model=list[StockReport])
def stock_report(db: Session = Depends(get_db)):
    products = db.query(Products).all()
    report = [
        StockReport(
            product_id=p.id,
            description=p.description,
            quantity=p.quantity,
            unit_price=float(p.price),
            total_value=float(p.price) * p.quantity
        )
        for p in products
    ]
    return report


@router.get("/sales", response_model=list[SaleSummary])
def sales_report(
    start_date: Optional[datetime.date] = None,
    end_date: Optional[datetime.date] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Sales)
    if start_date:
        query = query.filter(Sales.created_at >= start_date)
    if end_date:
        query = query.filter(Sales.created_at <= end_date)

    sales = query.all()
    report = []
    for s in sales:
        total_value = sum([float(item.unit_price) * item.quantity for item in s.items])
        report.append(
            SaleSummary(
                sale_id=s.id,
                client_name=s.client.name,
                operator_name=s.operator.name,
                total_value=total_value,
                created_at=s.created_at
            )
        )
    return report
