from fastapi import APIRouter
from app.api.v1.search import router as search_router
from app.api.v1.ingredients import router as ingredients_router
from app.api.v1.formulations import router as formulations_router

api_router = APIRouter()
api_router.include_router(search_router, prefix="/search", tags=["search"])
api_router.include_router(ingredients_router, prefix="/ingredients", tags=["ingredients"])
api_router.include_router(formulations_router, prefix="/formulations", tags=["formulations"])
