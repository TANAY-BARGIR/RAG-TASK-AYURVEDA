from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.core.config import get_settings
from app.core.limiter import limiter
from app.core.logger import logger
from app.api.v1 import api_router
from app.rag.retriever import retriever_instance
from app.rag.generator import generator_instance

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize Heavy Models on Startup
    logger.info("Application startup: Initializing services")
    retriever_instance.initialize()
    generator_instance.initialize()
    yield
    # Cleanup on shutdown
    logger.info("Application shutdown: Cleaning up resources")

settings = get_settings()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan
)

# Rate limiting (protects the billed NVIDIA embedding/LLM calls behind /search)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins_list,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Global Error Handler — never leak internal exception details to the client.
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled Exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"message": "Internal Server Error"},
    )

# Routers
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {"message": "Welcome to Ayurvedic Grantha Reference System API"}
