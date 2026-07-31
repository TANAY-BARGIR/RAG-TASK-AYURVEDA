import os
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings, ChatNVIDIA
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

load_dotenv()

def get_retrieval_pipeline():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    persistent_directory = os.path.join(script_dir, "..", "db", "chroma_db")
    
    if not os.path.exists(persistent_directory):
        raise Exception(f"Vector store not found at {persistent_directory}. Please run embedding_pipeline.py first.")

    embedding_model = NVIDIAEmbeddings(model="nvidia/nv-embedqa-e5-v5")
    vectorstore = Chroma(
        persist_directory=persistent_directory,
        embedding_function=embedding_model,
        collection_metadata={"hnsw:space": "cosine"}
    )
    
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

    llm = ChatNVIDIA(model="meta/llama-3.1-8b-instruct", temperature=0)

    prompt_template = """You are an expert Ayurvedic assistant. Your objective is to answer the user's question based strictly on the provided context passages. Do NOT use outside knowledge. Do not invent sources, pages, verses, or clinical recommendations.

If the context does not contain enough information to fully answer the question, you must state that there is insufficient information.

You must strictly output your response in the following structured format exactly:

Answer: [Concise response derived from the retrieved passage, or an insufficient-information refusal]
Source: [Document title(s) from the metadata, and any source texts/references mentioned in the text]
Location: [Geographical location if mentioned, or File name(s)/categories from metadata]
Evidence status: [Supported, Partially Supported, or Insufficient Evidence]

Context passages:
{context}

Question: {question}"""

    prompt = ChatPromptTemplate.from_template(prompt_template)

    def format_docs(docs):
        formatted_docs = []
        for i, doc in enumerate(docs):
            # Inject all metadata keys dynamically so no metadata is left behind
            meta_str = "\n".join([f"{str(k).capitalize()}: {str(v)}" for k, v in doc.metadata.items()])
            formatted_docs.append(f"--- Passage {i+1} ---\n{meta_str}\nContent:\n{doc.page_content}\n")
        return "\n".join(formatted_docs)

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain, retriever

def ask_question(question, rag_chain, retriever):
    print(f"\n{'='*50}\nQuestion: {question}\n{'-'*50}")
    
    docs = retriever.invoke(question)
    
    response = rag_chain.invoke(question)
    
    print(response)
    print("\nSupporting passages (Retrieval Trace):")
    for i, doc in enumerate(docs):
        print(f"  {i+1}. {doc.metadata.get('source_file')} - {doc.metadata.get('title')}")
    print("="*50)

def main():
    rag_chain, retriever = get_retrieval_pipeline()
    
    print("\n" + "="*50)
    print("🌿 Ayurvedic RAG Assistant Initialized 🌿")
    print("Type your question below, or type 'exit' to quit.")
    print("="*50)
    
    while True:
        try:
            q = input("\nYour Question: ")
            if q.strip().lower() in ['exit', 'quit']:
                print("Exiting...")
                break
            if q.strip():
                ask_question(q, rag_chain, retriever)
        except KeyboardInterrupt:
            print("\nExiting...")
            break

if __name__ == "__main__":
    main()
