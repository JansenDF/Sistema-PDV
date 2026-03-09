import json, bcrypt

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session, joinedload

from datetime import datetime, timedelta
from sqlalchemy import select
from decouple import config
from passlib.context import CryptContext
from jose import JWSError, jwt

from src.models.models import Users

SECRET_KEY = config("SECRET_KEY")
ALGORITHM = config("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = config("ACCESS_TOKEN_EXPIRE_MINUTES")

crypt_context = CryptContext(schemes=["sha256_crypt"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
expires_in = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def token_verify(token=Depends(oauth2_scheme)):
    service = LoginRepository()
    service.verify_token(token)

def verify_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))


class LoginRepository:

    __response401 = HTTPException(
                    detail="Usuário não autorizado.",
                    status_code=status.HTTP_401_UNAUTHORIZED
                )
    
    @classmethod
    def login(cls, username:str, password:str, db: Session):
        try:
            query = select(Users).where(Users.email == username)
            userdb = db.execute(query).scalars().first()
            if userdb is None:
                print("1")
                raise cls.__response401
            
            if not verify_password(password, userdb.password):
                print("2")
                raise cls.__response401
                
            exp = datetime.now() + timedelta(minutes=expires_in)
            payload = {
                "sub": json.dumps({"email": userdb.email, "name": userdb.name}),
                "exp": exp
            }
            access_token = jwt.encode(payload,key=SECRET_KEY, algorithm=ALGORITHM)
            return {"access_token": access_token, "email": userdb.email, "name": userdb.name, "id": userdb.id }
        except Exception as e:
            print("3")
            print(e)
            raise
        # finally:
        #     db.close()
    

    @classmethod
    def verify_token(cls, access_token, db: Session):
        try:
            data = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        except JWSError as e:
            print(e)
            raise
        
        js = json.loads(data['sub'])
        query = select(Users).where(Users.email == js['email'])
        userdb = db.execute(query).scalars().first()
        if userdb is None:
            raise cls.__response401
