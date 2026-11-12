from functools import lru_cache

from langchain.chat_models import init_chat_model

from app.core.config import settings


@lru_cache(maxsize=1)
def get_chat_model():
    if settings.groq_api_key is None:
        raise RuntimeError("GROQ_API_KEY is not configured.")

    return init_chat_model(
        model=settings.llm_model,
        model_provider="groq",
        api_key=settings.groq_api_key.get_secret_value(),
        temperature=0,
    )