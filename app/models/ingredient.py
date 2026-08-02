from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class Ingredient(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    botanical_name = Column(String, nullable=True)
    description = Column(String, nullable=True)
    category = Column(String, nullable=True)
    reference_id = Column(Integer, ForeignKey("references.id"), nullable=True)

    reference = relationship("Reference", back_populates="ingredients")
