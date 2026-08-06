from pydantic import BaseModel, Field
from typing import List, Optional, Any

class SearchQuery(BaseModel):
    query: str = Field(..., min_length=1, max_length=500)
    limit: int = Field(default=5, ge=1, le=20)

class SQLMatch(BaseModel):
    entity_type: str
    name: str
    details: Optional[str] = None

class RetrievedCitation(BaseModel):
    source_title: str
    chapter: Optional[str] = None
    verse: Optional[str] = None
    exact_passage: str
    similarity_score: float

class SearchResponse(BaseModel):
    query: str
    processing_time_ms: int
    confidence_score: float
    evidence_status: str
    generated_answer: Optional[str] = None
    sql_matches: List[SQLMatch] = []
    retrieved_citations: List[RetrievedCitation] = []
