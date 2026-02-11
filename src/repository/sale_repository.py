import bcrypt
import datetime
from fastapi import Depends, HTTPException, status

from sqlalchemy import select, update
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError

from src.schemas.sale_schemas import SaleCreate
from src.models.models import Sales, SaleItems, Products
from src.db.connectdb import get_db


class SaleRepository: 
    @classmethod
    def create_sale(cls, sale: SaleCreate, db: Session = Depends(get_db)):
        try:
            new_sale = Sales(
                operator_id=sale.operator_id,
                client_id=sale.client_id,
                created_at=datetime.datetime.now(),
                updated_at=datetime.datetime.now()
            )
            db.add(new_sale)

            # Cria os itens da venda
            for item in sale.items:
                product = db.query(Products).filter(Products.id == item.product_id).first()
                if not product:
                    raise HTTPException(status_code=404, detail="Produto não encontrado")
                if product.quantity < item.quantity:
                    raise HTTPException(status_code=400, detail="Estoque insuficiente")

                # Atualiza estoque
                product.quantity -= item.quantity
                product.updated_at = datetime.datetime.now()

                # Cria item da venda
                sale_item = SaleItems(
                    sale=new_sale,  # usa relação em vez de id
                    product_id=item.product_id,
                    quantity=item.quantity,
                    unit_price=item.unit_price,
                )
                db.add(sale_item)

            # Só faz commit depois de validar tudo
            db.commit()
            db.refresh(new_sale)

            return new_sale

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
                    sqlalchemybinaryexpression = (getattr(Sales, key)== params[key])
                else:
                    sqlalchemybinaryexpression = (getattr(Sales, key).like("%" +params[key]+ "%"))
                filters.append(sqlalchemybinaryexpression)

        try:
            select_sale = select(Sales).where(*filters)
            if params['skip'] is not None and params['limit'] is not None:
                salt = (params['skip'] * params['limit']) - params['limit']
                skip = 0 if salt < 0 else salt
                select_sale = select_sale.offset(skip).limit(params['limit'])
            sales = db.session.execute(select_sale).scalars().all()
            return sales
        except  IntegrityError as e:
            raise HTTPException(
                detail=e.orig.args[0],
                status_code=status.HTTP_400_BAD_REQUEST
            )
        finally:
            db.close()


    @classmethod
    def update_sale(cls, sale_id: int, sale_data: dict, db: Session):
        try:
            values_dict = {}
            for k, v in sale_data.items():
                if v is not None:
                    values_dict[k] = v

            values_dict["updated_at"] = datetime.datetime.now()

            query_update_sale = (
                update(Sales)
                .where(Sales.id == sale_id)
                .values(**values_dict)
                .execution_options(synchronize_session="fetch")
            )

            db.execute(query_update_sale)
            db.commit()

            updated_sale = db.query(Sales).filter(Sales.id == sale_id).first()
            return updated_sale

        except Exception as e:
            db.rollback()
            raise e
