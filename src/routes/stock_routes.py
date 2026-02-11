from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.db.connectdb import get_db
from src.models.models import Stocks
from src.schemas.stock_schemas import StockRead, StockCreate, StockUpdate
from src.repository.stock_repository import StockRepository


router = APIRouter(prefix="/stocks", tags=["Estoques"])

@router.post("/", response_model=StockRead)
def create_stocks(stock: StockCreate, db: Session = Depends(get_db)):
    try:
        db_stock = StockRepository.create_stock(stock=stock, db=db)
        return db_stock
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail="Não foi possível cadastrar o estoque")


@router.get("/", response_model=list[StockRead])
def read_stocks(db: Session = Depends(get_db)):
    return db.query(Stocks).all()


@router.get("/{stock_id}", response_model=StockRead)
def read_stock(stock_id: int, db: Session = Depends(get_db)):
    stock = db.query(Stocks).get(stock_id)
    if not stock:
        raise HTTPException(status_code=404, detail="Estoque não existe")
    return stock

@router.patch("/{stock_id}", response_model=StockRead)
def partial_update_stock(stock_id: int, stock: StockUpdate, db: Session = Depends(get_db)):
    
    has_stock = db.query(Stocks).get(stock_id)
    if not has_stock:
        raise HTTPException(status_code=404, detail="Estoque não existe")

    stock_data = stock.model_dump(exclude_unset=True)
    try:
        db_stock = StockRepository.update_stock(stock_id=stock_id, stock_data=stock_data, db=db)
        return db_stock
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="Erro ao atualizar estoque")