from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.api.dependencies import get_db, verify_api_key
from app.schemas.formulation import Formulation, FormulationCreate
from app.repositories.formulation import formulation

router = APIRouter()

@router.post("/", response_model=Formulation, dependencies=[Depends(verify_api_key)])
def create_formulation(obj_in: FormulationCreate, db: Session = Depends(get_db)):
    return formulation.create(db, obj_in=obj_in)

@router.get("/", response_model=List[Formulation])
def get_formulations(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    db: Session = Depends(get_db),
):
    return formulation.get_multi(db, skip=skip, limit=limit)

@router.get("/{id}", response_model=Formulation)
def get_formulation(id: int, db: Session = Depends(get_db)):
    db_obj = formulation.get(db, id=id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Formulation not found")
    return db_obj
