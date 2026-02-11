from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.db.connectdb import get_db
from src.models.models import Clients
from src.schemas.client_schemas import ClientRead, ClientCreate, ClientUpdate
from src.repository.client_repository import ClientRepository


router = APIRouter(prefix="/clients", tags=["Clientes"])

@router.post("/", response_model=ClientRead)
def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    try:
        db_client = ClientRepository.create_client(client=client, db=db)
        return db_client
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail="Não foi possível cadastrar o cliente")


@router.get("/", response_model=list[ClientRead])
def read_clients(db: Session = Depends(get_db)):
    return db.query(Clients).all()


@router.get("/{client_id}", response_model=ClientRead)
def read_client(client_id: int, db: Session = Depends(get_db)):
    client = db.query(Clients).get(client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Cliente não existe")
    return client


@router.patch("/{client_id}", response_model=ClientRead)
def partial_update_client(client_id: int, client: ClientUpdate, db: Session = Depends(get_db)):

    has_client = db.query(Clients).get(client_id)
    if not has_client:
        raise HTTPException(status_code=404, detail="Cliente não existe")
    
    client_data = client.model_dump(exclude_unset=True)
    try:
        db_client = ClientRepository.update_client(client_id=client_id, client_data=client_data, db=db)
        return db_client
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="Erro ao atualizar cliente")