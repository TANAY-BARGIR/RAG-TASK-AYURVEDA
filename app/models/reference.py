from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class Reference(Base):
    __tablename__ = "references"

    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(Integer, ForeignKey("sources.id"))
    edition = Column(String, nullable=True)
    volume = Column(String, nullable=True)
    chapter = Column(String, nullable=True)
    section = Column(String, nullable=True)
    page = Column(String, nullable=True)
    verse = Column(String, nullable=True)
    original_text = Column(String, nullable=True)
    translation = Column(String, nullable=True)

    source = relationship("Source", back_populates="references")
    ingredients = relationship("Ingredient", back_populates="reference")
    formulations = relationship("Formulation", back_populates="reference")
