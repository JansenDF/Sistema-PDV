from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.db.connectdb import get_db
from src.models.models import Products
from src.schemas.product_schema import ProductRead, ProductCreate, ProductUpdate
from src.repository.product_repository import ProductRepository


router = APIRouter(prefix="/products", tags=["Produtos"])

@router.post("/", response_model=ProductRead)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    try:
        db_product = ProductRepository.create_product(product=product, db=db)
        return db_product
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail="Não foi possível cadastrar o produto")


@router.get("/", response_model=list[ProductRead])
def read_products(db: Session = Depends(get_db)):
    return db.query(Products).all()


@router.get("/{product_id}", response_model=ProductRead)
def read_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Products).get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Produto não existe")
    return product


@router.patch("/{product_id}", response_model=ProductRead)
def partial_update_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):

    has_product = db.query(Products).get(product_id)
    if not has_product:
        raise HTTPException(status_code=404, detail="Produto não existe")

    product_data = product.model_dump(exclude_unset=True)
    try:
        db_product = ProductRepository.update_product(product_id=product_id, product_data=product_data, db=db)
        return db_product
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="Erro ao atualizar produto")