from app.repositories.base import CRUDBase
from app.models.ingredient import Ingredient
from app.schemas.ingredient import IngredientCreate

class CRUDIngredient(CRUDBase[Ingredient, IngredientCreate]):
    pass

ingredient = CRUDIngredient(Ingredient)
