from brevo import AsyncBrevo

from app.core.config import settings


def get_brevo_client() -> AsyncBrevo:
    if settings.brevo_api_key is None:
        raise RuntimeError("BREVO_API_KEY is not configured.")

    return AsyncBrevo(
        api_key=settings.brevo_api_key.get_secret_value(),
        timeout=30.0,
    )