from fastapi import FastAPI ,HTTPException
from contextlib import asynccontextmanager
from services.retrieval_pipeline import get_retrieval_pipeline
from service_backend.models import QueryRequest, QueryResponse
import re


@asynccontextmanager
async def lifespan(app:FastAPI):
    print("Loading Vector Store and LLM.....")

    try:
        rag_chain , retriever = get_retrieval_pipeline()
        app.state.rag_chain = rag_chain
        app.state.retriever = retriever
        print("Models loaded successfully!")
    except Exception as e:
        print(f"Failed to load RAG pipeline: {e}")

    yield

    print("Shutting down and cleaning up...")


app = FastAPI(title="Ayurvedic RAG Microservice", lifespan=lifespan)

@app.post("/ask", response_model= QueryResponse)
async def ask_question(request:QueryRequest):
        if not hasattr(app.state,"rag_chain"):
             raise HTTPException(500,"RAG Pipepline not initialised")

        try:
            raw_response = app.state.rag_chain.invoke(request.question)
        except:
            raise HTTPException(500,"Empty Response")

        try:
            # Search the response for the "Answer:" section.
            # Capture all text after "Answer:" until the next "Source:" marker.
            # The lookahead (?=\nSource:) stops the match before "Source:" without including it.
            answer = re.search(r'Answer:\s*(.*?)(?=\nSource:)',raw_response,re.DOTALL).group(1).strip()
            # Extract captured answer and trim leading/trailing whitespace

            source = re.search(r'Source:\s*(.*?)(?=\nLocation:)',raw_response,re.DOTALL).group(1).strip()

            location = re.search(r'Location:\s*(.*?)(?=\nEvidence status:)', raw_response, re.DOTALL).group(1).strip()

            evidence = re.search(r'Evidence status:\s*(.*)', raw_response, re.DOTALL).group(1).strip()

            return QueryResponse(
                 answer=answer,
                 source=source,
                 location=location,
                 evidence_status=evidence,
                 raw_output=raw_response
            )

        except Exception as e:
            return QueryResponse(
            answer="Failed to parse structured output.",
            source="N/A",
            location="N/A",
            evidence_status="Error",
            raw_output=raw_response
        )