import datetime
from fastapi import Depends, HTTPException, status

from sqlalchemy import select, update
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.schemas.product_sub_category_schemas import ProductSubCategoryCreate
from src.models.models import ProductSubCategory
from src.db.connectdb import get_db


class ProductSubCategoryRepository: 
    
    @classmethod
    def create_product_sub_category(cls, product_sub_category: ProductSubCategoryCreate, db: Session = Depends(get_db)):
        try:
            new_category = ProductSubCategory(
                description=product_sub_category.description,
                product_category_id=product_sub_category.product_category_id,
                created_at=datetime.datetime.now(),
                updated_at=datetime.datetime.now()
            )
            db.add(new_category)
            db.commit()
            db.refresh(new_category)
            return new_category
        except Exception as e:
            print(e)
            db.rollback()
            raise

    
    @classmethod
    def find_all(cls, params, db: Session = Depends(get_db)):
        filters =[]
        for key in params:
            if params[key] is not None and key != 'skip' and key != 'limit':
                if isinstance( params[key], int):
                    sqlalchemybinaryexpression = (getattr(ProductSubCategory, key)== params[key])
                else:
                    sqlalchemybinaryexpression = (getattr(ProductSubCategory, key).like("%" +params[key]+ "%"))
                filters.append(sqlalchemybinaryexpression)

        try:
            select_category = select(ProductSubCategory).where(*filters)
            if params['skip'] is not None and params['limit'] is not None:
                salt = (params['skip'] * params['limit']) - params['limit']
                skip = 0 if salt < 0 else salt
                select_category = select_category.offset(skip).limit(params['limit'])
            category = db.session.execute(select_category).scalars().all()
            return category
        except  IntegrityError as e:
            raise HTTPException(
                detail=e.orig.args[0],
                status_code=status.HTTP_400_BAD_REQUEST
            )
        finally:
            db.close()


    @classmethod
    def update_product_sub_category(cls, product_sub_category_id: int, product_sub_category_data: dict, db: Session):
        try:
            values_dict = {}
            for k, v in product_sub_category_data.items():
                if v is not None:
                    values_dict[k] = v

            values_dict["updated_at"] = datetime.datetime.now()

            query_update_category = (
                update(ProductSubCategory)
                .where(ProductSubCategory.id == product_sub_category_id)
                .values(**values_dict)
                .execution_options(synchronize_session="fetch")
            )

            db.execute(query_update_category)
            db.commit()

            updated_supplier = db.query(ProductSubCategory).filter(ProductSubCategory.id == product_sub_category_id).first()
            return updated_supplier

        except Exception as e:
            db.rollback()
            raise e
