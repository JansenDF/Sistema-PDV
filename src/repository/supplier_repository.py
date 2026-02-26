import datetime
from fastapi import Depends, HTTPException, status

from sqlalchemy import select, update
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.schemas.supplier_schemas import SupplierCreate
from src.models.models import Suppliers
from src.db.connectdb import get_db


class SupplierRepository: 
    
    @classmethod
    def create_supplier(cls, supplier: SupplierCreate, db: Session = Depends(get_db)):
        try:
            new_supplier = Suppliers(
                company_name=supplier.company_name,
                created_at=datetime.datetime.now(),
                updated_at=datetime.datetime.now()
            )
            db.add(new_supplier)
            db.commit()
            db.refresh(new_supplier)
            return new_supplier
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
                    sqlalchemybinaryexpression = (getattr(Suppliers, key)== params[key])
                else:
                    sqlalchemybinaryexpression = (getattr(Suppliers, key).like("%" +params[key]+ "%"))
                filters.append(sqlalchemybinaryexpression)

        try:
            select_supplier = select(Suppliers).where(*filters)
            if params['skip'] is not None and params['limit'] is not None:
                salt = (params['skip'] * params['limit']) - params['limit']
                skip = 0 if salt < 0 else salt
                select_supplier = select_supplier.offset(skip).limit(params['limit'])
            supplier = db.session.execute(select_supplier).scalars().all()
            return supplier
        except  IntegrityError as e:
            raise HTTPException(
                detail=e.orig.args[0],
                status_code=status.HTTP_400_BAD_REQUEST
            )
        finally:
            db.close()


    @classmethod
    def update_supplier(cls, supplier_id: int, supplier_data: dict, db: Session):
        try:
            values_dict = {}
            for k, v in supplier_data.items():
                if v is not None:
                    values_dict[k] = v

            values_dict["updated_at"] = datetime.datetime.now()

            query_update_supplier = (
                update(Suppliers)
                .where(Suppliers.id == supplier_id)
                .values(**values_dict)
                .execution_options(synchronize_session="fetch")
            )

            db.execute(query_update_supplier)
            db.commit()

            updated_supplier = db.query(Suppliers).filter(Suppliers.id == supplier_id).first()
            return updated_supplier

        except Exception as e:
            db.rollback()
            raise e
