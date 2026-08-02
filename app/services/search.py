import time
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.schemas.search import SearchQuery, SearchResponse, SQLMatch
from app.models.ingredient import Ingredient
from app.models.formulation import Formulation
from app.rag.pipeline import process_query
from app.core.logger import logger

class SearchService:
    def __init__(self, db: Session):
        self.db = db

    def search(self, query: SearchQuery) -> SearchResponse:
        start_time = time.time()
        
        # 1. Query Normalization
        normalized_query = query.query.strip().lower()
        
        # 2. SQL Exact & Fuzzy Search (Basic implementation for SQLite)
        sql_matches = []
        
        # Escape SQL LIKE wildcards in user input so "%"/"_" can't be used to
        # widen matches beyond what the user actually typed.
        escaped_query = (
            normalized_query.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
        )
        like_pattern = f"%{escaped_query}%"

        # Search Ingredients
        ingredients = self.db.query(Ingredient).filter(
            or_(
                Ingredient.name.ilike(like_pattern, escape="\\"),
                Ingredient.botanical_name.ilike(like_pattern, escape="\\")
            )
        ).limit(query.limit).all()

        for ing in ingredients:
            sql_matches.append(SQLMatch(
                entity_type="Ingredient",
                name=ing.name,
                details=ing.description or ing.botanical_name
            ))

        # Search Formulations
        formulations = self.db.query(Formulation).filter(
            Formulation.name.ilike(like_pattern, escape="\\")
        ).limit(query.limit).all()

        for form in formulations:
            sql_matches.append(SQLMatch(
                entity_type="Formulation",
                name=form.name,
                details=form.therapeutic_use or form.preparation_method
            ))

        # 3. Vector Retrieval & LLM Generation
        rag_result = process_query(query.query, top_k=query.limit)
        
        processing_time_ms = int((time.time() - start_time) * 1000)
        
        return SearchResponse(
            query=query.query,
            processing_time_ms=processing_time_ms,
            confidence_score=rag_result["confidence_score"],
            evidence_status=rag_result["evidence_status"],
            generated_answer=rag_result["generated_answer"],
            sql_matches=sql_matches,
            retrieved_citations=rag_result["retrieved_citations"]
        )
