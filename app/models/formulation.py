from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class Formulation(Base):
    __tablename__ = "formulations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    preparation_method = Column(String, nullable=True)
    therapeutic_use = Column(String, nullable=True)
    reference_id = Column(Integer, ForeignKey("references.id"), nullable=True)

    reference = relationship("Reference", back_populates="formulations")
