"""LLM integration"""
from langchain_openai import ChatOpenAI
from app.core.config import settings


def get_llm():
    """Get LLM instance"""
    return ChatOpenAI(
        model=settings.LLM_MODEL,
        api_key=settings.OPENAI_API_KEY,
        temperature=0.7
    )
