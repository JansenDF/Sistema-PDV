from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.db.connectdb import get_db
from src.models.models import Products
from src.schemas.stock_schemas import StockReport
from src.repository.purchase_repository import PurchaseRepository


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
