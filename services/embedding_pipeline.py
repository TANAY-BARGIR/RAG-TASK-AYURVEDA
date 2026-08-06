import re,os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings
from langchain_core.documents import Document
from langchain_chroma import Chroma
from dotenv import load_dotenv

load_dotenv()

# Must match app.core.config.Settings.CHROMA_COLLECTION_NAME. LangChain's
# Chroma wrapper silently defaults to a collection named "langchain" if this
# isn't passed explicitly, which previously caused the API's retriever (which
# looks up a named collection) to find nothing.
COLLECTION_NAME = "ayurveda_texts"

def load_documents(path):
    with open(path,'r',encoding='utf-8') as f:
        content  = f.read()

    raw_docs = re.split(r'^# Document: ', content, flags=re.MULTILINE)

    extracted_data = []

    for raw_doc in raw_docs:
        if not raw_doc.strip():
            continue

        parts = re.split(r'^## Metadata\n|^## Content\n', raw_doc, flags=re.MULTILINE)

        if len(parts) < 3:
            continue
            
        filename = parts[0].strip()
        metadata_text = parts[1].strip()
        body_text = parts[2].strip()

        doc_metadata = {"source_file": filename}

        for line in metadata_text.split('\n'):
            if line.startswith('- '):
                meta_item = line[2:].strip()

                if ':' in meta_item:
                    key, val = meta_item.split(':', 1)
                    doc_metadata[key.strip()] = val.strip(' "\'')

        extracted_data.append({
            "content": body_text,
            "metadata": doc_metadata
        })
            
    return extracted_data

def split_documents(extracted_data):
    text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=150,
            separators=["\n\n", "\n", ".", " ", ""]
    )

    final_chunks = []
    for item in extracted_data:
        chunk_texts = text_splitter.split_text(item["content"])
        
        for chunk_text in chunk_texts:
            final_chunks.append(Document(
                page_content=chunk_text,
                metadata=item["metadata"]
            ))

    return final_chunks

def create_vector_store(chunks, persist_directory="db/chroma_db"):
    """Create and persist ChromaDB vector store"""
    print("Creating embeddings and storing in ChromaDB...")
        
    embedding_model = NVIDIAEmbeddings(model="nvidia/nv-embedqa-e5-v5")
    
    # Create ChromaDB vector store
    print("--- Creating vector store ---")
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=persist_directory,
        collection_name=COLLECTION_NAME,
        collection_metadata={"hnsw:space": "cosine"}
    )
    print("--- Finished creating vector store ---")
    
    print(f"Vector store created and saved to {persist_directory}")
    return vectorstore


def main():
    """Main ingestion pipeline"""
    print("=== RAG Document Ingestion Pipeline ===\n")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(script_dir, "..", "data", "Traditions.md")
    persistent_directory = os.path.join(script_dir, "..", "db", "chroma_db")
    
    if os.path.exists(persistent_directory):
        print("Vector store already exists. No need to re-process documents.")
        
        embedding_model = NVIDIAEmbeddings(model="nvidia/nv-embedqa-e5-v5")
        vectorstore = Chroma(
            persist_directory=persistent_directory,
            embedding_function=embedding_model,
            collection_name=COLLECTION_NAME,
            collection_metadata={"hnsw:space": "cosine"}
        )
        print(f"Loaded existing vector store with {vectorstore._collection.count()} documents")
        return vectorstore
    
    print("Persistent directory does not exist. Initializing vector store...\n")
    
    documents = load_documents(path)  

    chunks = split_documents(documents)
    
    vectorstore = create_vector_store(chunks, persistent_directory)
    
    print("\nIngestion complete! Your documents are now ready for RAG queries.")
    return vectorstore

if __name__ == "__main__":
    main()