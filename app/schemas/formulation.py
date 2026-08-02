from pydantic import BaseModel, ConfigDict
from typing import Optional
from app.schemas.base import Reference

class FormulationBase(BaseModel):
    name: str
    preparation_method: Optional[str] = None
    therapeutic_use: Optional[str] = None
    reference_id: Optional[int] = None

class FormulationCreate(FormulationBase):
    pass

class Formulation(FormulationBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    reference: Optional[Reference] = None
