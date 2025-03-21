import requests
import json
from requests.auth import HTTPBasicAuth

def whats_app_api(phone, code): 
    account_sid = "credenciais"
    auth_token = "credenciais"
    url = f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json"

    response = requests.post(
        url,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "To": f"whatsapp:{phone}",  # Usa o telefone do usuário
            "From": "whatsapp:+14155238886",
            "ContentSid": "credenciais",
            "ContentVariables": json.dumps({"code": code}),  # Passa o código corretamente
        },
        auth=HTTPBasicAuth(account_sid, auth_token),
    )
    print(response.text)
