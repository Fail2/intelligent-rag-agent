
from brevo.core.api_error import ApiError
from brevo.transactional_emails import (
    SendTransacEmailRequestSender,
    SendTransacEmailRequestToItem,
)

from app.core.config import settings
from app.email.client import get_brevo_client


async def send_email(subject: str, body: str, recipient_email: str | None = None, recipient_name: str | None = None,) -> str:
    """Send a transactional email through Brevo."""

    to_email = recipient_email or settings.default_recipient_email

    client = get_brevo_client()

    try:
        result = await client.transactional_emails.send_transac_email(
            subject=subject,
            text_content=body,
            sender=SendTransacEmailRequestSender(
                name=settings.brevo_sender_name,
                email=settings.brevo_sender_email,
            ),
            to=[
                SendTransacEmailRequestToItem(
                    email=to_email,
                    name=recipient_name,
                )
            ],
        )

        return result.message_id

    except ApiError:
        raise
