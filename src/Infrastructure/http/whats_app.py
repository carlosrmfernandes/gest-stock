import requests
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv

load_dotenv()

def whats_app_api(phone, code): 
    account_sid = os.getenv('SID')
    auth_token = os.getenv('TOKEN')
    url = f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json"

    data = {
        "To": f"whatsapp:{phone}",
        "From": "whatsapp:+14155238886",
        "Body": f"Seu código de verificação é: {code}"
    }

    response = requests.post(
        url,
        data=data,
        auth=HTTPBasicAuth(account_sid, auth_token)
    )

    print(response.status_code)
    print(response.text)
