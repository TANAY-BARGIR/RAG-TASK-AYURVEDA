# RAG-TASK-AYURVEDA

This project implements a **Citation-Backed Retrieval-Augmented Generation (RAG) System** for querying Ayurvedic knowledge. It prioritizes strict metadata preservation, precise source attribution, and prevents hallucination when handling domain-specific inquiries.

## 🏗️ Architecture & Steps Taken

### 1. Data Preprocessing & Formatting (`data/`)
- **Corpus Consolidation:** Merged 30 individual Ayurvedic `.md` files into a single master document (`Traditions.md`).
- **Data Cleansing:** Stripped all image links (`![alt](url)` and HTML `<img>` tags) to ensure purely semantic textual content.
- **Metadata Structure:** Re-formatted the document so that every sub-document begins with a strict `# Document: ` header and includes its YAML frontmatter (title, categories, date, file name) under a `## Metadata` section.

### 2. Embedding & Ingestion Pipeline (`services/embedding_pipeline.py`)
- **Custom Document Parsing:** Replaced naive `DirectoryLoader` with custom regex parsing to separate the metadata block from the main content block.
- **Metadata-Aware Chunking:** Utilized LangChain's `RecursiveCharacterTextSplitter` (chunk size: 1000, overlap: 150) strictly on the content blocks, while explicitly attaching the parsed metadata dictionary to every resulting `Document` chunk.
- **Vector Storage:** Generated embeddings using `NVIDIAEmbeddings` (`nvidia/nv-embedqa-e5-v5`) and persisted the data locally using ChromaDB.

### 3. Retrieval & QA Pipeline (`services/retrieval_pipeline.py`)
- **Strict Prompt Engineering:** Developed a constrained prompt template instructing the LLM (`meta/llama-3.1-8b-instruct` via `ChatNVIDIA`) to exclusively use the provided context and strictly adhere to a 4-line output format (`Answer`, `Source`, `Location`, `Evidence status`).
- **Contextual Injection:** Formatted the retrieved ChromaDB chunks to prominently display all metadata directly inside the LLM context window to ensure flawlessly accurate citation mapping.
- **Hallucination Prevention:** The prompt effectively limits the model from inventing sources, ensuring it returns `Insufficient information` / `Insufficient Evidence` when queried with out-of-context terms.

## 🚀 Setup Instructions

1. **Create Virtual Environment & Install Dependencies:**
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install langchain langchain-community langchain-text-splitters langchain-chroma chromadb python-dotenv langchain-nvidia-ai-endpoints
   ```

2. **Configure Environment:**
   Ensure you have an `.env` file at the project root containing your API keys (e.g., `NVIDIA_API_KEY`).

3. **Run Ingestion Pipeline:**
   ```bash
   python services/embedding_pipeline.py
   ```
   *(This creates the `db/chroma_db` directory locally).*

4. **Run Retrieval Pipeline (Evaluation Tests):**
   ```bash
   python services/retrieval_pipeline.py
   ```

### 5. Running as a FastAPI Microservice (`service_backend/`)
To expose this RAG pipeline as a stateless API service for a frontend:
1. Install additional dependencies:
   ```bash
   pip install fastapi uvicorn
   ```
2. Run the Uvicorn server from the **root** `RAG TASK` directory:
   ```bash
   uvicorn service_backend.app:app --reload
   ```
3. Test the endpoint:
   - Make a POST request to `http://localhost:8000/ask` with JSON body: `{"question": "Your question here"}`
   - Or explore the interactive Swagger UI at `http://localhost:8000/docs`
