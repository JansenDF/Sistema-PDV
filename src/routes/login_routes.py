from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from src.repository.login_repository import LoginRepository
from sqlalchemy.orm import Session

from src.db.connectdb import get_db

router = APIRouter(prefix="/login", tags=["Login"])

service = LoginRepository()

@router.post("/")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    usr = service.login(username=form_data.username, password=form_data.password, db=db)
    return usr