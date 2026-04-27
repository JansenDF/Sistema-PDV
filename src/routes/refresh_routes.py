import json
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from sqlalchemy import select
from src.db.connectdb import get_db
from src.models.models import Users
from decouple import config
from pydantic import BaseModel


SECRET_KEY = config("SECRET_KEY")
ALGORITHM = config("ALGORITHM")
REFRESH_TOKEN_EXPIRE_DAYS = config("REFRESH_TOKEN_EXPIRE_DAYS")
ACCESS_TOKEN_EXPIRE_MINUTES = int(config("ACCESS_TOKEN_EXPIRE_MINUTES"))


class RefreshRequest(BaseModel):
    refresh_token: str


router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/refresh")
def refresh_token(request: RefreshRequest, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(request.refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
        user_data = json.loads(payload["sub"])
        query = select(Users).where(Users.email == user_data["email"])
        userdb = db.execute(query).scalars().first()
        if not userdb:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não encontrado")

        expires_in = ACCESS_TOKEN_EXPIRE_MINUTES
        # Gera novo access token
        exp_access = datetime.utcnow() + timedelta(minutes=expires_in)
        payload_access = {
            "sub": json.dumps({"email": userdb.email, "name": userdb.name}),
            "exp": exp_access,
            "type": "access"
        }
        new_access_token = jwt.encode(payload_access, key=SECRET_KEY, algorithm=ALGORITHM)

        return {"access_token": new_access_token, "token_type": "bearer"}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token inválido")
