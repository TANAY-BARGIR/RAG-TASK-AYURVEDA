from pydantic import BaseModel, ConfigDict
from typing import Optional
from app.schemas.base import Reference

class IngredientBase(BaseModel):
    name: str
    botanical_name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    reference_id: Optional[int] = None

class IngredientCreate(IngredientBase):
    pass

class Ingredient(IngredientBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    reference: Optional[Reference] = None
