import datetime
from fastapi import Depends, HTTPException, status

from sqlalchemy import select, update
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.schemas.purchase_schemas import PurchaseCreate
from src.models.models import Purchases, PurchasesItems, Products
from src.db.connectdb import get_db


class PurchaseRepository: 
    @classmethod
    def create_purchase(cls, purchase: PurchaseCreate, db: Session = Depends(get_db)):
        try:
            new_purchase = Purchases(
                supplier_id=purchase.supplier_id,
                stock_id=purchase.stock_id,
                created_at=datetime.datetime.now(),
                updated_at=datetime.datetime.now()
            )
            db.add(new_purchase)

            # Cria os itens da venda
            for item in purchase.items:
                product = db.query(Products).filter(Products.id == item.product_id).first()
                if not product:
                    raise HTTPException(status_code=404, detail="Produto não encontrado")
                if product.quantity < item.quantity:
                    raise HTTPException(status_code=400, detail="Estoque insuficiente")

                # Atualiza estoque
                product.quantity += item.quantity
                product.updated_at = datetime.datetime.now()

                # Cria item da venda
                purchase_item = PurchasesItems(
                    purchase=new_purchase,  # usa relação em vez de id
                    product_id=item.product_id,
                    quantity=item.quantity,
                    unit_price=item.unit_price,
                )
                db.add(purchase_item)

            # Só faz commit depois de validar tudo
            db.commit()
            db.refresh(new_purchase)

            return new_purchase

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
                    sqlalchemybinaryexpression = (getattr(Purchases, key)== params[key])
                else:
                    sqlalchemybinaryexpression = (getattr(Purchases, key).like("%" +params[key]+ "%"))
                filters.append(sqlalchemybinaryexpression)

        try:
            select_purchase = select(Purchases).where(*filters)
            if params['skip'] is not None and params['limit'] is not None:
                salt = (params['skip'] * params['limit']) - params['limit']
                skip = 0 if salt < 0 else salt
                select_purchase = select_purchase.offset(skip).limit(params['limit'])
            purchase = db.session.execute(select_purchase).scalars().all()
            return purchase
        except  IntegrityError as e:
            raise HTTPException(
                detail=e.orig.args[0],
                status_code=status.HTTP_400_BAD_REQUEST
            )
        finally:
            db.close()


    @classmethod
    def update_purchase(cls, purchase_id: int, purchase_data: dict, db: Session):
        try:
            values_dict = {}
            for k, v in purchase_data.items():
                if v is not None:
                    values_dict[k] = v

            values_dict["updated_at"] = datetime.datetime.now()

            query_update_purchase = (
                update(Purchases)
                .where(Purchases.id == purchase_id)
                .values(**values_dict)
                .execution_options(synchronize_session="fetch")
            )

            db.execute(query_update_purchase)
            db.commit()

            updated_purchase = db.query(Purchases).filter(Purchases.id == purchase_id).first()
            return updated_purchase

        except Exception as e:
            db.rollback()
            raise e
