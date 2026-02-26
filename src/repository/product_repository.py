import bcrypt
import datetime
from fastapi import Depends, HTTPException, status

from sqlalchemy import select, update
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError

from src.schemas.user_schemas import UserCreate, UserUpdate
from src.schemas.product_schema import ProductCreate
from src.models.models import Products
from src.db.connectdb import get_db


class ProductRepository: 
    
    @classmethod
    def create_product(cls, product: ProductCreate, db: Session = Depends(get_db)):
        try:
            new_product = Products(
                description=product.description,
                quantity=product.quantity,
                price=product.price,
                stock_id=product.stock_id,
                created_at=datetime.datetime.now(),
                updated_at=datetime.datetime.now()
            )
            db.add(new_product)
            db.commit()
            db.refresh(new_product)
            return new_product
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
                    sqlalchemybinaryexpression = (getattr(Products, key)== params[key])
                else:
                    sqlalchemybinaryexpression = (getattr(Products, key).like("%" +params[key]+ "%"))
                filters.append(sqlalchemybinaryexpression)

        try:
            select_product = select(Products).where(*filters)
            if params['skip'] is not None and params['limit'] is not None:
                salt = (params['skip'] * params['limit']) - params['limit']
                skip = 0 if salt < 0 else salt
                select_product = select_product.offset(skip).limit(params['limit'])
            products = db.session.execute(select_product).scalars().all()
            return products
        except  IntegrityError as e:
            raise HTTPException(
                detail=e.orig.args[0],
                status_code=status.HTTP_400_BAD_REQUEST
            )
        finally:
            db.close()


    @classmethod
    def update_product(cls, product_id: int, product_data: dict, db: Session):
        try:
            values_dict = {}
            for k, v in product_data.items():
                if v is not None:
                    values_dict[k] = v

            values_dict["updated_at"] = datetime.datetime.now()

            query_update_product = (
                update(Products)
                .where(Products.id == product_id)
                .values(**values_dict)
                .execution_options(synchronize_session="fetch")
            )

            db.execute(query_update_product)
            db.commit()

            updated_product = db.query(Products).filter(Products.id == product_id).first()
            return updated_product

        except Exception as e:
            db.rollback()
            raise e
