from langchain_google_genai import GoogleGenerativeAIEmbeddings

from app.core.config import settings


def get_embeddings() -> GoogleGenerativeAIEmbeddings:
    """Initialize Google Gemini embeddings using application settings.

    Function: get_embeddings
    Args:
        None.
    Returns:
        GoogleGenerativeAIEmbeddings: Configured embedding model.
    """
    if not settings.google_api_key:
        raise ValueError("GOOGLE_API_KEY is not configured.")

    return GoogleGenerativeAIEmbeddings(
        model=settings.embedding_model,
        google_api_key=settings.google_api_key,
    )