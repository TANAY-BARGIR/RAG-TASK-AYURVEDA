from app.repositories.base import CRUDBase
from app.models.formulation import Formulation
from app.schemas.formulation import FormulationCreate

class CRUDFormulation(CRUDBase[Formulation, FormulationCreate]):
    pass

formulation = CRUDFormulation(Formulation)
