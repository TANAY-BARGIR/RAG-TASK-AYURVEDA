from pydantic import BaseModel

class QueryRequest(BaseModel):
    question:str

class QueryResponse(BaseModel):
    answer:str
    source:str
    location:str
    evidence_status:str
    raw_output:str
    