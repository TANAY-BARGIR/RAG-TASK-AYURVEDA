from app.rag.retriever import retriever_instance
from app.rag.generator import generator_instance
from app.core.config import get_settings
from app.core.logger import logger
from typing import Dict, Any

def process_query(query: str, top_k: int = None) -> Dict[str, Any]:
    settings = get_settings()

    # 1. Retrieve citations
    citations = retriever_instance.retrieve(query, top_k=top_k)
    
    if not citations:
        return {
            "evidence_status": "Insufficient Evidence",
            "confidence_score": 0.0,
            "generated_answer": "No relevant texts found.",
            "retrieved_citations": []
        }
        
    # 2. Determine confidence and evidence status
    max_score = max(c["similarity_score"] for c in citations)
    
    if max_score > settings.SUPPORTED_THRESHOLD:
        evidence_status = "Supported"
    elif max_score > settings.PARTIAL_THRESHOLD:
        evidence_status = "Partially Supported"
    else:
        evidence_status = "Insufficient Evidence"
        
    # 3. Format citations for response
    formatted_citations = []
    context_blocks = []
    
    for c in citations:
        meta = c["metadata"]
        passage = c["exact_passage"]
        
        formatted_citations.append({
            "source_title": meta.get("title", "Unknown Source"),
            "chapter": meta.get("chapter"),
            "verse": meta.get("verse"),
            "exact_passage": passage,
            "similarity_score": c["similarity_score"]
        })
        context_blocks.append(f"[Source: {meta.get('title', 'Unknown')}]\n{passage}")
        
    # 4. Generate answer if sufficient evidence
    if evidence_status == "Insufficient Evidence":
        generated_answer = "The retrieved texts do not provide sufficient evidence to answer this query."
    else:
        context_str = "\n\n".join(context_blocks)
        generated_answer = generator_instance.generate(query, context_str)
        
    return {
        "evidence_status": evidence_status,
        "confidence_score": max_score,
        "generated_answer": generated_answer,
        "retrieved_citations": formatted_citations
    }
