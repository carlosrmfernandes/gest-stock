import os

from twilio.rest import Client

from src.Application.Ports.message_service_port import MessageServicePort


def _build_twilio_client():
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")

    if not account_sid or not auth_token:
        return None

    return Client(account_sid, auth_token)


class TwilioMessageService(MessageServicePort):
    def send_activation(self, celular, codigo):
        client = _build_twilio_client()
        if client is None:
            raise RuntimeError(
                "Twilio credentials are missing. Set TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN."
            )

        message = client.messages.create(
            from_="whatsapp:+14155238886",
            to=f"whatsapp:+{celular}",
            content_sid="HX229f5a04fd0510ce1b071852155d3e75",
            content_variables=f'{{"1":"{codigo}"}}',
        )

        return {
            "sid": message.sid,
            "status": message.status,
            "to": message.to,
        }
