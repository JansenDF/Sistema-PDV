from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.db.connectdb import get_db
from src.models.models import Sales
from src.schemas.sale_schemas import SaleRead, SaleCreate, SaleUpdate
from src.repository.sale_repository import SaleRepository


router = APIRouter(prefix="/sales", tags=["Vendas"])

@router.post("/", response_model=SaleRead)
def create_sale(sale: SaleCreate, db: Session = Depends(get_db)):
    try:
        db_sale = SaleRepository.create_sale(sale=sale, db=db)
        return db_sale
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Erro no servidor - {e}")


@router.get("/", response_model=list[SaleRead])
def read_sales(db: Session = Depends(get_db)):
    return db.query(Sales).all()


@router.get("/{sale_id}", response_model=SaleRead)
def read_sale(sale_id: int, db: Session = Depends(get_db)):
    sale = db.query(Sales).get(sale_id)
    if not sale:
        raise HTTPException(status_code=404, detail="Venda não existe")
    return sale


@router.patch("/{sale_id}", response_model=SaleRead)
def partial_update_sale(sale_id: int, sale: SaleUpdate, db: Session = Depends(get_db)):

    has_sale = db.query(Sales).get(sale_id)
    if not has_sale:
        raise HTTPException(status_code=404, detail="Venda não existe")
    
    sale_data = sale.model_dump(exclude_unset=True)
    try:
        db_sale = SaleRepository.update_sale(sale_id=sale_id, sale_data=sale_data, db=db)
        return db_sale
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="Erro ao atualizar venda")