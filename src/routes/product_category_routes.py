from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.db.connectdb import get_db
from src.models.models import ProductCategory
from src.schemas.product_category_schemas import (
    ProductCategoryRead, ProductCategoryCreate, ProductCategoryUpdate
)
from src.repository.product_category_repository import ProductCategoryRepository


router = APIRouter(prefix="/product_categories", tags=["Categorias de Produtos"])

@router.post("/", response_model=ProductCategoryRead)
def create_category(product_category: ProductCategoryCreate, db: Session = Depends(get_db)):
    try:
        db_product_category = ProductCategoryRepository.create_product_category(
            product_category=product_category, db=db
        )
        return db_product_category
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail="Não foi possível cadastrar a  categoria")


@router.get("/", response_model=list[ProductCategoryRead])
def read_product_category(db: Session = Depends(get_db)):
    return db.query(ProductCategory).all()


@router.get("/{product_category_id}", response_model=ProductCategoryRead)
def read_product_category(product_category_id: int, db: Session = Depends(get_db)):
    product_category = db.query(ProductCategory).get(product_category_id)
    if not product_category:
        raise HTTPException(status_code=404, detail="Categoria não existe")
    return product_category


@router.patch("/{product_category_id}", response_model=ProductCategoryRead)
def partial_update_product_category(
    product_category_id: int, 
    product_category: ProductCategoryUpdate, 
    db: Session = Depends(get_db)
):

    has_product_category = db.query(ProductCategory).get(product_category_id)
    if not has_product_category:
        raise HTTPException(status_code=404, detail="Categoria não existe")
    
    product_category_data = product_category.model_dump(exclude_unset=True)
    try:
        db_product_category = ProductCategoryRepository.update_product_category(
            product_category_id=product_category_id, 
            product_category_data=product_category_data, 
            db=db
        )
        return db_product_category
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="Erro ao atualizar categoria do produto")
