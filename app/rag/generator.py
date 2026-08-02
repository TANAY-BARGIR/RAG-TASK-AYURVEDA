from langchain_nvidia_ai_endpoints import ChatNVIDIA
from app.core.config import get_settings
from app.core.logger import logger
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

class LLMGenerator:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LLMGenerator, cls).__new__(cls)
            cls._instance.chain = None
        return cls._instance

    def initialize(self):
        settings = get_settings()
        try:
            self.llm = ChatNVIDIA(
                model="meta/llama-3.1-70b-instruct",
                nvidia_api_key=settings.NVIDIA_API_KEY,
                temperature=0.0
            )
            self.prompt = ChatPromptTemplate.from_messages([
                ("system", "You are an expert Ayurvedic assistant. Answer the user's question based strictly on the provided context. If the context does not contain the answer, say 'I cannot answer this based on the provided texts.' Do not hallucinate citations, only generate the natural language answer."),
                ("user", "Context:\n{context}\n\nQuestion: {question}")
            ])
            self.chain = self.prompt | self.llm | StrOutputParser()
            logger.info("LLMGenerator initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize LLMGenerator: {e}")
            self.chain = None

    def generate(self, question: str, context: str) -> str:
        if not self.chain:
            return "LLM service is not available."
        
        try:
            response = self.chain.invoke({
                "context": context,
                "question": question
            })
            return response
        except Exception as e:
            logger.error(f"Error during LLM generation: {e}")
            return "An error occurred during generation."

generator_instance = LLMGenerator()
