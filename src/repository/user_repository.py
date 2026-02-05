import bcrypt
import datetime
from fastapi import Depends, HTTPException, status

from sqlalchemy import select, update
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError

from src.schemas.user_schemas import UserCreate, UserUpdate
from src.models.models import Users
from src.db.connectdb import get_db


# Função para criar um hash da senha
def hash_password(password):
    # Gerar um salt
    salt = bcrypt.gensalt(rounds=6)
    # Criar o hash da senha
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


# Função para verificar a senha
def check_password(hashed_password, password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))


class UserRepository: 
    
    @classmethod
    def create_user(cls, user: UserCreate, db: Session = Depends(get_db)):
        try:
            new_user = Users(
                name=user.name,
                email=user.email,
                password=hash_password(user.password),
                created_at=datetime.datetime.now()
            )
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            return new_user
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
                    sqlalchemybinaryexpression = (getattr(Users, key)== params[key])
                else:
                    sqlalchemybinaryexpression = (getattr(Users, key).like("%" +params[key]+ "%"))
                filters.append(sqlalchemybinaryexpression)

        try:
            select_user = select(Users).where(*filters)
            if params['skip'] is not None and params['limit'] is not None:
                salt = (params['skip'] * params['limit']) - params['limit']
                skip = 0 if salt < 0 else salt
                select_user = select_user.offset(skip).limit(params['limit'])
            users = db.session.execute(select_user).scalars().all()
            return users
        except  IntegrityError as e:
            raise HTTPException(
                detail=e.orig.args[0],
                status_code=status.HTTP_400_BAD_REQUEST
            )
        finally:
            db.close()

    
    @classmethod
    def update_user(cls, user_id: int, user, db: Session = Depends(get_db)):
        try:
            values_dict = {}
            for k, v in user:
                if v:
                    values_dict[k] = v
            # values_dict["updated"] = datetime.datetime.now()
            values_dict["password"] = hash_password(values_dict["password"])
            for field, value in values_dict.items():
                setattr(user, field, value)
            print(values_dict)
            query_update_user = update(Users).where(Users.id == user_id).values(values_dict)
            db.session.execute(query_update_user)
            db.session.commit()
            updated_user = db.session.query(Users).filter(Users.id == user_id).first()
            return updated_user
        except Exception as e:
            print(e)
            db.session.rollback()
            raise Exception
        finally:
            db.close()