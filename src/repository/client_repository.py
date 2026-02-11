import bcrypt
import datetime
from fastapi import Depends, HTTPException, status

from sqlalchemy import select, update
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError

from src.schemas.client_schemas import ClientCreate
from src.models.models import Clients
from src.db.connectdb import get_db


class ClientRepository: 
    
    @classmethod
    def create_client(cls, client: ClientCreate, db: Session = Depends(get_db)):
        try:
            new_client = Clients(
                name=client.name,
                created_at=datetime.datetime.now(),
                updated_at=datetime.datetime.now()
            )
            db.add(new_client)
            db.commit()
            db.refresh(new_client)
            return new_client
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
                    sqlalchemybinaryexpression = (getattr(Clients, key)== params[key])
                else:
                    sqlalchemybinaryexpression = (getattr(Clients, key).like("%" +params[key]+ "%"))
                filters.append(sqlalchemybinaryexpression)

        try:
            select_client = select(Clients).where(*filters)
            if params['skip'] is not None and params['limit'] is not None:
                salt = (params['skip'] * params['limit']) - params['limit']
                skip = 0 if salt < 0 else salt
                select_client = select_client.offset(skip).limit(params['limit'])
            clients = db.session.execute(select_client).scalars().all()
            return clients
        except  IntegrityError as e:
            raise HTTPException(
                detail=e.orig.args[0],
                status_code=status.HTTP_400_BAD_REQUEST
            )
        finally:
            db.close()


    @classmethod
    def update_client(cls, client_id: int, client_data: dict, db: Session):
        try:
            values_dict = {}
            for k, v in client_data.items():
                if v is not None:
                    values_dict[k] = v

            values_dict["updated_at"] = datetime.datetime.now()

            query_update_client = (
                update(Clients)
                .where(Clients.id == client_id)
                .values(**values_dict)
                .execution_options(synchronize_session="fetch")
            )

            db.execute(query_update_client)
            db.commit()

            updated_client = db.query(Clients).filter(Clients.id == client_id).first()
            return updated_client

        except Exception as e:
            db.rollback()
            raise e
