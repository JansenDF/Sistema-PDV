from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.db.connectdb import get_db
from src.models.models import Suppliers
from src.schemas.supplier_schemas import SupplierRead, SupplierCreate, SupplierUpdate
from src.repository.supplier_repository import SupplierRepository


router = APIRouter(prefix="/suppliers", tags=["Fornecedores"])

@router.post("/", response_model=SupplierRead)
def create_supplier(supplier: SupplierCreate, db: Session = Depends(get_db)):
    try:
        db_supplier = SupplierRepository.create_supplier(supplier=supplier, db=db)
        return db_supplier
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail="Não foi possível cadastrar o fornecedor")


@router.get("/", response_model=list[SupplierRead])
def read_suppliers(db: Session = Depends(get_db)):
    return db.query(Suppliers).all()


@router.get("/{supplier_id}", response_model=SupplierRead)
def read_supplier(supplier_id: int, db: Session = Depends(get_db)):
    supplier = db.query(Suppliers).get(supplier_id)
    if not supplier:
        raise HTTPException(status_code=404, detail="Fornecedor não existe")
    return supplier


@router.patch("/{supplier_id}", response_model=SupplierRead)
def partial_update_supplier(supplier_id: int, supplier: SupplierUpdate, db: Session = Depends(get_db)):

    has_supplier = db.query(Suppliers).get(supplier_id)
    if not has_supplier:
        raise HTTPException(status_code=404, detail="Fornecedor não existe")
    
    supplier_data = supplier.model_dump(exclude_unset=True)
    try:
        db_supplier = SupplierRepository.update_supplier(supplier_id=supplier_id, supplier_data=supplier_data, db=db)
        return db_supplier
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="Erro ao atualizar fornecedor")
