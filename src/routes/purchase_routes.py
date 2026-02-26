from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.db.connectdb import get_db
from src.models.models import Purchases
from src.schemas.purchase_schemas import PurchaseRead, PurchaseCreate, PurchaseUpdate
from src.repository.purchase_repository import PurchaseRepository


router = APIRouter(prefix="/purchase", tags=["Compras"])

@router.post("/", response_model=PurchaseRead)
def create_purchase(purchase: PurchaseCreate, db: Session = Depends(get_db)):
    try:
        db_purchase = PurchaseRepository.create_purchase(purchase=purchase, db=db)
        return db_purchase
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Erro no servidor - {e}")


@router.get("/", response_model=list[PurchaseRead])
def read_purchase(db: Session = Depends(get_db)):
    return db.query(Purchases).all()


@router.get("/{purchase_id}", response_model=PurchaseRead)
def read_purchase(purchase_id: int, db: Session = Depends(get_db)):
    purchase = db.query(Purchases).get(purchase_id)
    if not purchase:
        raise HTTPException(status_code=404, detail="Compra não existe")
    return purchase


@router.patch("/{purchase_id}", response_model=PurchaseRead)
def partial_update_purchase(purchase_id: int, purchase: PurchaseUpdate, db: Session = Depends(get_db)):

    has_purchase = db.query(Purchases).get(purchase_id)
    if not has_purchase:
        raise HTTPException(status_code=404, detail="Compra não existe")
    
    purchase_data = purchase.model_dump(exclude_unset=True)
    try:
        db_purchase = PurchaseRepository.update_purchase(purchase_id=purchase_id, sale_data=purchase_data, db=db)
        return db_purchase
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="Erro ao atualizar compra")