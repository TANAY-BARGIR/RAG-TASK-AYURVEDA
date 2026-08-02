from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.core.config import get_settings
from app.core.limiter import limiter
from app.schemas.search import SearchQuery, SearchResponse
from app.services.search import SearchService

router = APIRouter()

@router.post("/", response_model=SearchResponse)
@limiter.limit(lambda: get_settings().SEARCH_RATE_LIMIT)
def search_system(request: Request, query: SearchQuery, db: Session = Depends(get_db)):
    search_service = SearchService(db)
    return search_service.search(query)
