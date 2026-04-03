from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.db.connectdb import get_db
from src.models.models import ProductSubCategory
from src.schemas.product_sub_category_schemas import (
    ProductSubCategoryRead, ProductSubCategoryCreate, ProductSubCategoryUpdate
)
from src.repository.product_sub_category_repository import ProductSubCategoryRepository


router = APIRouter(prefix="/product_sub_categories", tags=["Sub Categorias de Produtos"])

@router.post("/", response_model=ProductSubCategoryRead)
def create_category(product_sub_category: ProductSubCategoryCreate, db: Session = Depends(get_db)):
    try:
        db_product_sub_category = ProductSubCategoryRepository.create_product_sub_category(
            product_sub_category=product_sub_category, db=db
        )
        return db_product_sub_category
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail="Não foi possível cadastrar a sub categoria")


@router.get("/", response_model=list[ProductSubCategoryRead])
def read_product_sub_category(db: Session = Depends(get_db)):
    return db.query(ProductSubCategory).order_by(ProductSubCategory.description.asc()).all()


@router.get("/{product_sub_category_id}", response_model=ProductSubCategoryRead)
def read_product_sub_category(product_sub_category_id: int, db: Session = Depends(get_db)):
    product_sub_category = db.query(ProductSubCategory).get(product_sub_category_id)
    if not product_sub_category:
        raise HTTPException(status_code=404, detail="Sub categoria não existe")
    return product_sub_category


@router.patch("/{product_sub_category_id}", response_model=ProductSubCategoryRead)
def partial_update_product_sub_category(
    product_sub_category_id: int, 
    product_sub_category: ProductSubCategoryUpdate, 
    db: Session = Depends(get_db)
):

    has_product_sub_category = db.query(ProductSubCategory).get(product_sub_category_id)
    if not has_product_sub_category:
        raise HTTPException(status_code=404, detail="Sub categoria não existe")
    
    product_sub_category_data = product_sub_category.model_dump(exclude_unset=True)
    try:
        db_product_sub_category = ProductSubCategoryRepository.update_product_sub_category(
            product_sub_category_id=product_sub_category_id, 
            product_sub_category_data=product_sub_category_data, 
            db=db
        )
        return db_product_sub_category
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="Erro ao atualizar fornecedor")
