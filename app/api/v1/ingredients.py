from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.api.dependencies import get_db, verify_api_key
from app.schemas.ingredient import Ingredient, IngredientCreate
from app.repositories.ingredient import ingredient

router = APIRouter()

@router.post("/", response_model=Ingredient, dependencies=[Depends(verify_api_key)])
def create_ingredient(obj_in: IngredientCreate, db: Session = Depends(get_db)):
    return ingredient.create(db, obj_in=obj_in)

@router.get("/", response_model=List[Ingredient])
def get_ingredients(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    db: Session = Depends(get_db),
):
    return ingredient.get_multi(db, skip=skip, limit=limit)

@router.get("/{id}", response_model=Ingredient)
def get_ingredient(id: int, db: Session = Depends(get_db)):
    db_obj = ingredient.get(db, id=id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    return db_obj
