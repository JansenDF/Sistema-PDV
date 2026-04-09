import datetime
from datetime import datetime as dt, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from src.schemas.sold_schemas import SoldBase
from src.db.connectdb import get_db
from src.models.models import Products, Sales, SaleItems
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
                created_at=s.created_at,
                date=s.date
            )
        )
    return report


@router.get("/sold-products", response_model=list[SoldBase])
def sold_products(
    days: int = Query(7, ge=1, le=30),  # filtro: últimos 7, 15 ou 30 dias
    db: Session = Depends(get_db)
):
    """
    Retorna os produtos vendidos nos últimos X dias.
    """

    limite = dt.utcnow() - timedelta(days=days)

    query = (
        db.query(
            Products.id.label("id"),
            Products.description.label("description"),
            func.sum(SaleItems.quantity).label("quantity"),
            func.sum(SaleItems.quantity * SaleItems.unit_price).label("total_value"),
        )
        .join(SaleItems, SaleItems.product_id == Products.id)
        .join(Sales, Sales.id == SaleItems.sale_id)
        .filter(Sales.created_at >= limite)
        .group_by(Products.id, Products.description)
        .order_by(func.sum(SaleItems.quantity).desc())
    )

    return query.all()
