import os
import requests

from src.Domain.exceptions import NotificationError

TWILIO_BASE_URL = 'https://api.twilio.com/2010-04-01'


class WhatsAppClient:
    """
    Cliente HTTP do provedor externo (Twilio) para envio do código de ativação.

    Esta classe é a fronteira da aplicação com o mundo externo:
    nenhum teste unitário deve fazer requisição de verdade aqui.
    Ela existe para ser substituída por um mock (ou ter o `requests.post` patchado).
    """

    def __init__(self, account_sid=None, auth_token=None, from_number=None, timeout=10):
        self.account_sid = account_sid or os.getenv('TWILIO_ACCOUNT_SID', 'fake-sid')
        self.auth_token = auth_token or os.getenv('TWILIO_AUTH_TOKEN', 'fake-token')
        self.from_number = from_number or os.getenv('TWILIO_FROM', '+5511000000000')
        self.timeout = timeout

    def send_message(self, to, body):
        """
        Envia a mensagem e devolve o id da mensagem no provedor.

        Levanta NotificationError se o provedor responder erro
        ou se a requisição falhar (timeout, rede fora, etc).
        """
        url = f'{TWILIO_BASE_URL}/Accounts/{self.account_sid}/Messages.json'
        payload = {'To': to, 'From': self.from_number, 'Body': body}

        try:
            response = requests.post(
                url,
                data=payload,
                auth=(self.account_sid, self.auth_token),
                timeout=self.timeout,
            )
        except requests.RequestException as exc:
            raise NotificationError(f'Falha ao contatar o provedor de mensagens: {exc}')

        if response.status_code >= 400:
            raise NotificationError(
                f'Provedor de mensagens retornou erro {response.status_code}'
            )

        return response.json().get('sid')


class ActivationNotifier:
    """
    Regra de apresentação da mensagem de ativação.
    Recebe o client por injeção de dependência — é isso que torna o serviço testável.
    """

    MESSAGE_TEMPLATE = 'Seu codigo de ativacao no Gest Stock e: {code}'

    def __init__(self, client=None):
        self.client = client or WhatsAppClient()

    def send_activation_code(self, phone, code):
        body = self.MESSAGE_TEMPLATE.format(code=code)
        return self.client.send_message(to=phone, body=body)
