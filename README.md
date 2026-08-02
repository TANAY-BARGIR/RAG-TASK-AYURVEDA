# RAG-TASK-AYURVEDA

This project implements a **Citation-Backed Retrieval-Augmented Generation (RAG) System** for querying Ayurvedic knowledge. It prioritizes strict metadata preservation, precise source attribution, and prevents hallucination when handling domain-specific inquiries.

## 🏗️ Architecture

### 1. Data Preprocessing & Formatting (`data/`)
- **Corpus Consolidation:** Merged 30 individual Ayurvedic `.md` files into a single master document (`Traditions.md`).
- **Data Cleansing:** Stripped all image links (`![alt](url)` and HTML `<img>` tags) to ensure purely semantic textual content.
- **Metadata Structure:** Re-formatted the document so that every sub-document begins with a strict `# Document: ` header and includes its YAML frontmatter (title, categories, date, file name) under a `## Metadata` section.

### 2. Embedding & Ingestion Pipeline (`services/embedding_pipeline.py`)
- **Custom Document Parsing:** Replaced naive `DirectoryLoader` with custom regex parsing to separate the metadata block from the main content block.
- **Metadata-Aware Chunking:** Utilized LangChain's `RecursiveCharacterTextSplitter` (chunk size: 1000, overlap: 150) strictly on the content blocks, while explicitly attaching the parsed metadata dictionary to every resulting `Document` chunk.
- **Vector Storage:** Generated embeddings using `NVIDIAEmbeddings` (`nvidia/nv-embedqa-e5-v5`) and persisted the data locally using ChromaDB, under the named collection `ayurveda_texts` (see `app/core/config.py`).

### 3. Web API (`app/`)
The ingestion pipeline above feeds a layered FastAPI backend:
- **`app/api/v1/`** — routes: `POST/GET /ingredients`, `POST/GET /formulations`, `POST /search`.
- **`app/models/` + `app/repositories/`** — SQLAlchemy models and data-access layer for structured `Ingredient`/`Formulation`/`Reference`/`Source` records, migrated via **Alembic** (`alembic/`).
- **`app/schemas/`** — Pydantic request/response contracts, with input bounds (query length, pagination limits) enforced at the boundary.
- **`app/rag/`** — `retriever.py` (Chroma + NVIDIA embeddings), `generator.py` (Llama 3.1 via ChatNVIDIA), `pipeline.py` (orchestrates retrieval → confidence thresholding → generation). Citations returned to the client come directly from the retrieved Chroma metadata, never from parsing the LLM's free-text output, so they can't be hallucinated.
- **`app/services/search.py`** — combines an exact SQL match (ingredients/formulations) with the semantic RAG result into one response.

**Security/reliability baked in:** write endpoints require an `ADMIN_API_KEY` header (fails closed if unset), CORS is an explicit origin allowlist, `/search` is rate-limited (it triggers billed NVIDIA calls), and the global error handler never leaks internal exception details to clients.

## 🚀 Setup Instructions

1. **Install dependencies:**
   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configure environment:**
   Copy `.env.example` to `.env` and fill in `NVIDIA_API_KEY` (and `ADMIN_API_KEY` if you need to create ingredients/formulations).

3. **Run the ingestion pipeline** (only needed if `db/chroma_db` doesn't already exist or you're re-embedding new source text):
   ```bash
   python services/embedding_pipeline.py
   ```

4. **Apply database migrations:**
   ```bash
   alembic upgrade head
   ```

5. **Run the API:**
   ```bash
   uvicorn app.main:app --reload
   ```
   - Interactive docs: `http://localhost:8000/docs`
   - Search: `POST http://localhost:8000/api/v1/search/` with JSON body `{"query": "your question", "limit": 5}`

6. **Run tests:**
   ```bash
   python -m pytest
   ```
