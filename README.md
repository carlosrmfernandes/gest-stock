# Gest-Stock API

Projeto backend em Flask para cadastro de vendedores/usuários de mini mercado, com persistência local (SQLite por padrão) e suporte opcional a MySQL + Docker.

## Visão Geral

Atualmente, esta API inclui:

- Endpoints de saúde
- Cadastro de vendedor/usuário (`/user`)
- Integração com envio de mensagem de ativação via WhatsApp (Twilio)
- Estrutura no estilo Hexagonal (Ports and Adapters)

## Stack Tecnológica

- Python 3.8
- Flask 3
- SQLAlchemy / Flask-SQLAlchemy
- Twilio SDK
- Docker / Docker Compose (opcional para MySQL e app em container)

## Estrutura do Projeto

```text
.
|-- run.py
|-- docker-compose.yml
|-- Dockerfile
|-- requirements.txt
`-- src/
    |-- routes.py
    |-- config/
    |   `-- data_base.py
    |-- Domain/
    |   `-- user.py
    |-- Application/
    |   |-- Controllers/user_controller.py
    |   |-- Ports/
    |   |   |-- message_service_port.py
    |   |   `-- user_repository_port.py
    |   `-- UseCases/user_use_case.py
    |-- Infrastructure/
    |   |-- Model/user.py
    |   `-- Adapters/
    |       |-- messaging/twilio_message_service.py
    |       `-- repositories/sqlalchemy_user_repository.py
```

## Variáveis de Ambiente (`.env`)

Crie um arquivo `.env` na raiz do projeto:

```env
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
```

Observações:

- Essas variáveis são obrigatórias para envio de mensagens no WhatsApp.
- Se estiverem ausentes, a aplicação sobe, mas os envios via Twilio retornam erro.
- Não faça commit de credenciais reais no git.

## Banco de Dados

O projeto está configurado em `src/config/data_base.py` com duas opções:

1. SQLite (padrão)
- Ativo por padrão
- Arquivo do banco: `market_management.db`
- Ideal para desenvolvimento local

2. MySQL (Docker)
- Nome do serviço no compose: `mysql57`
- Imagem: `mysql:8.0.29`
- Banco: `market_management`
- Mapeamento de porta: `127.0.0.1:3306:3306`

Para trocar de SQLite para MySQL, atualize `SQLALCHEMY_DATABASE_URI` em `src/config/data_base.py` conforme indicado nos comentários.

## Executando o Projeto

### Opção 1: Local (sem Docker)

1. Crie e ative um ambiente virtual.
2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Defina as variáveis de ambiente (`.env` ou exports no shell).
4. Execute:

```bash
flask --app run.py run
```

A API ficará disponível em `http://localhost:5000`.

### Opção 2: Docker Compose

1. Garanta que o `.env` existe com as variáveis do Twilio.
2. Execute:

```bash
docker compose up --build
```

Containers:

- `web`: API Flask em `http://localhost:5000`
- `mysql57`: MySQL em `127.0.0.1:3306`

## Endpoints da API

Base URL: `http://localhost:5000`

### `GET /`

Health check.

Exemplo de resposta:

```json
{
  "message": "Server is running"
}
```

### `GET /api`

Endpoint de status da API.

Exemplo de resposta:

```json
{
  "mensagem": "API - OK; Docker - Up"
}
```

### `POST /user`

Cria um usuário/vendedor e dispara o envio de ativação no WhatsApp via Twilio.

Corpo da requisição:

```json
{
  "nome": "Mini Mercado X",
  "cnpj": "12345678000199",
  "email": "mercado@email.com",
  "celular": "5511999999999",
  "senha": "123456"
}
```

Resposta de sucesso (`200`):

```json
{
  "mensagem": "Usuario salvo com sucesso. Verifique o WhatsApp.",
  "usuarios cadastrados": {},
  "whatsapp": {
    "sid": "SMxxxxxxxx",
    "status": "queued",
    "to": "whatsapp:+5511999999999"
  }
}
```

Possíveis erros:

- `400`: campo obrigatório ausente
- `401`: CNPJ inválido ou tamanho de telefone inválido
- `502`: usuário criado, mas falha no envio via WhatsApp

### `GET /testarNumero`

Envia uma mensagem de WhatsApp via Twilio para um número fixo (teste de integração).

Resposta de sucesso (`200`):

```json
{
  "sid": "SMxxxxxxxx",
  "status": "queued",
  "to": "whatsapp:+5511958942521"
}
```

Resposta de erro (`500`):

```json
{
  "erro": "..."
}
```

### `GET /users`

Lista todos os usuários.

## Comandos cURL Úteis

Criar usuário:

```bash
curl -X POST http://localhost:5000/user \
  -H "Content-Type: application/json" \
  -d "{\"nome\":\"Mini Mercado X\",\"cnpj\":\"12345678000199\",\"email\":\"mercado@email.com\",\"celular\":\"5511999999999\",\"senha\":\"123456\"}"
```

Status da API:

```bash
curl http://localhost:5000/api
```

Teste Twilio:

```bash
curl http://localhost:5000/testarNumero
```