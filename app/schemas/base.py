from pydantic import BaseModel, ConfigDict
from typing import Optional

class SourceBase(BaseModel):
    title: str
    author: Optional[str] = None
    description: Optional[str] = None

class Source(SourceBase):
    model_config = ConfigDict(from_attributes=True)
    id: int

class ReferenceBase(BaseModel):
    edition: Optional[str] = None
    volume: Optional[str] = None
    chapter: Optional[str] = None
    section: Optional[str] = None
    page: Optional[str] = None
    verse: Optional[str] = None
    original_text: Optional[str] = None
    translation: Optional[str] = None

class Reference(ReferenceBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    source_id: Optional[int]
