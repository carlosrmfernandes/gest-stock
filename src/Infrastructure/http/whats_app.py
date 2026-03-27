from twilio.rest import Client
from flask import current_app

def twilio_whatsapp_code(phone, code):

    try:
        account_sid = current_app.config["TWILIO_ACCOUNT_SID"]
        auth_token = current_app.config["TWILIO_AUTH_TOKEN"]
        twilio_number = current_app.config["TWILIO_WHATSAPP_NUMBER"]

        client = Client(account_sid, auth_token)

        message = client.messages.create(
            body=f"Seu código de ativação é: {code}",
            from_=twilio_number,
            to=f"whatsapp:+55{phone}"
        )
        print("Mensagem enviada:", message.sid)
        return message.sid

    except Exception as e:
        print("Erro Twilio:", e)
        return None