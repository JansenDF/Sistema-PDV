import bcrypt
import datetime
from fastapi import Depends, HTTPException, status

from sqlalchemy import select, update
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError

from src.schemas.user_schemas import UserCreate, UserUpdate
from src.schemas.stock_schemas import StockCreate
from src.models.models import Users, Stocks
from src.db.connectdb import get_db


class StockRepository: 
    
    @classmethod
    def create_stock(cls, stock: StockCreate, db: Session = Depends(get_db)):
        try:
            new_stock = Stocks(
                description=stock.description,
                created_at=datetime.datetime.now(),
                updated_at=datetime.datetime.now()
            )
            db.add(new_stock)
            db.commit()
            db.refresh(new_stock)
            return new_stock
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
                    sqlalchemybinaryexpression = (getattr(Stocks, key) == params[key])
                else:
                    sqlalchemybinaryexpression = (getattr(Stocks, key).like("%" +params[key]+ "%"))
                filters.append(sqlalchemybinaryexpression)

        try:
            select_stock = select(Stocks).where(*filters)
            if params['skip'] is not None and params['limit'] is not None:
                salt = (params['skip'] * params['limit']) - params['limit']
                skip = 0 if salt < 0 else salt
                select_stock = select_stock.offset(skip).limit(params['limit'])
            stocks = db.session.execute(select_stock).scalars().all()
            return stocks
        except  IntegrityError as e:
            raise HTTPException(
                detail=e.orig.args[0],
                status_code=status.HTTP_400_BAD_REQUEST
            )
        finally:
            db.close()


    @classmethod
    def update_stock(cls, stock_id: int, stock_data: dict, db: Session):
        try:
            values_dict = {}
            for k, v in stock_data.items():
                if v is not None:
                    values_dict[k] = v

            values_dict["updated_at"] = datetime.datetime.now()

            query_update_stock = (
                update(Stocks)
                .where(Stocks.id == stock_id)
                .values(**values_dict)
                .execution_options(synchronize_session="fetch")
            )

            db.execute(query_update_stock)
            db.commit()

            updated_stock = db.query(Stocks).filter(Stocks.id == stock_id).first()
            return updated_stock

        except Exception as e:
            db.rollback()
            raise e
