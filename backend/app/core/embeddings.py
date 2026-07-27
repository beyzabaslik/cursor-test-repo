"""Embeddings integration"""
from langchain_openai import OpenAIEmbeddings
from app.core.config import settings


def get_embeddings():
    """Get embeddings instance"""
    return OpenAIEmbeddings(
        model=settings.EMBEDDING_MODEL,
        api_key=settings.OPENAI_API_KEY
    )
