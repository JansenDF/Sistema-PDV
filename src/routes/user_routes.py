from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.db.connectdb import get_db
from src.models.models import Users
from src.schemas.user_schemas import UserCreate, UserRead, UserUpdate
from src.repository.user_repository import UserRepository


router = APIRouter(prefix="/users", tags=["Usuários"])

@router.post("/", response_model=UserRead)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = UserRepository.create_user(user=user, db=db)
        return db_user
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail="Não foi possível cadastrar o usuário")


@router.get("/", response_model=list[UserRead])
def read_users(db: Session = Depends(get_db)):
    return db.query(Users).all()


@router.get("/{user_id}", response_model=UserRead)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(Users).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não existe")
    return user

from src.schemas.user_schemas import UserUpdate  # Certifique-se de ter esse schema


@router.patch("/{user_id}", response_model=UserRead)
def partial_update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):

    has_user = db.query(Users).get(user_id)
    if not has_user:
        raise HTTPException(status_code=404, detail="Usuário não existe")
    
    user_data = user.model_dump(exclude_unset=True)
    try:
        db_user = UserRepository.update_user(user_id=user_id, user_data=user_data, db=db)
        return db_user
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="Erro ao atualizar usuário")