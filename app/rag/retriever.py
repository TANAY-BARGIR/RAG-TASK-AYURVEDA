import chromadb
from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings
from app.core.config import get_settings
from app.core.logger import logger

class ChromaRetriever:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ChromaRetriever, cls).__new__(cls)
            cls._instance.collection = None
            cls._instance.embeddings = None
        return cls._instance

    def initialize(self):
        settings = get_settings()
        self.persist_directory = settings.CHROMA_PERSIST_DIRECTORY
        try:
            self.embeddings = NVIDIAEmbeddings(
                model="nvidia/nv-embedqa-e5-v5",
                nvidia_api_key=settings.NVIDIA_API_KEY
            )
            self.client = chromadb.PersistentClient(path=self.persist_directory)
            self.collection = self.client.get_collection(name=settings.CHROMA_COLLECTION_NAME)
            logger.info("ChromaRetriever initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize ChromaRetriever: {e}")
            self.collection = None

    def retrieve(self, query: str, top_k: int = None):
        if not self.collection:
            return []
        
        settings = get_settings()
        k = top_k or settings.TOP_K_RETRIEVAL
        k = max(1, min(k, settings.MAX_TOP_K_RETRIEVAL))

        try:
            query_embedding = self.embeddings.embed_query(query)
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=k,
                include=["documents", "metadatas", "distances"]
            )
            
            citations = []
            for i in range(len(results["documents"][0])):
                doc = results["documents"][0][i]
                metadata = results["metadatas"][0][i]
                distance = results["distances"][0][i]
                
                # Convert distance to similarity score
                similarity = 1.0 - (distance / 2.0)
                
                citations.append({
                    "exact_passage": doc,
                    "similarity_score": similarity,
                    "metadata": metadata
                })
                
            return citations
        except Exception as e:
            logger.error(f"Error during retrieval: {e}")
            return []

retriever_instance = ChromaRetriever()
