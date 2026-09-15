# 🧪 Prova P1 — Automação de Testes

**Projeto:** Gest Stock — Gestão de Estoque para Mini Mercados
**Branch:** `p1`
**Stack de testes:** `pytest` + `unittest.mock`

---

## 📌 O que você precisa fazer

O sistema **já está implementado**. Sua tarefa é **escrever os testes**.

Você vai testar dois fluxos:

1. **Cadastro e ativação de Seller** (mini mercado), incluindo o envio do código por WhatsApp/SMS
2. **Cadastro de Produto**

> ⚠️ **Não altere o código de produção** (`src/`). Se você acha que encontrou um bug,
> **escreva um teste que prove o bug** e explique no docstring. Isso vale ponto extra.

---

## 🚀 Preparando o ambiente

```bash
git checkout p1

python -m venv .venv
.venv\Scripts\activate         # Windows
source .venv/bin/activate      # Linux/Mac

pip install -r requirements.txt

pytest                                       # roda os testes
pytest --cov=src --cov-report=term-missing   # roda com cobertura
```

Para subir a API e explorar manualmente:

```bash
python run.py        # http://localhost:5000/api
```

---

## 🏛️ Arquitetura (onde está cada coisa)

```
src/
├── Domain/                              ← regras puras, sem framework
│   ├── seller.py                        SellerDomain (is_active, matches_code)
│   ├── product.py                       ProductDomain
│   ├── validators.py                    is_valid_cnpj, is_valid_email, is_valid_phone...
│   └── exceptions.py                    ValidationError, ConflictError, NotFoundError...
│
├── Application/
│   ├── Service/
│   │   ├── seller_service.py            ★ create_seller / activate_seller
│   │   ├── product_service.py           ★ create_product / list_products
│   │   └── activation_code.py           generate_activation_code (usa random)
│   └── Controllers/                     camada HTTP (traduz erro → status code)
│
└── Infrastructure/
    ├── Model/                           tabelas SQLAlchemy
    ├── Repository/                      ← MOCKE ISTO (acesso ao banco)
    └── http/whats_app.py                ← MOCKE ISTO (provedor externo Twilio)
```

★ = onde está a maior parte das regras de negócio que você deve testar.

**Todos os serviços recebem suas dependências pelo construtor.** É assim que você injeta os mocks:

```python
service = SellerService(repository=meu_mock, notifier=outro_mock, code_generator=lambda: '1234')
```

---

## 🔧 Regra de ouro dos mocks

Seus testes de unidade **não podem**:

- ❌ tocar no banco de dados
- ❌ fazer requisição HTTP de verdade para o Twilio
- ❌ depender do `random` (o código de ativação precisa ser determinístico no teste)
- ❌ depender de ordem de execução entre testes

Tudo isso deve ser substituído por **dublês de teste** (`Mock`, `MagicMock`, `patch`).

### Fixtures que já estão prontas para você

O arquivo [`tests/conftest.py`](tests/conftest.py) já traz:

| Fixture | O que é |
|---|---|
| `seller_repository` | Mock do `SellerRepository` (banco vazio por padrão) |
| `product_repository` | Mock do `ProductRepository` |
| `notifier` | Mock do `ActivationNotifier` (envio de mensagem) |
| `code_generator` | Gerador determinístico — sempre retorna `'1234'` |
| `seller_payload` | Dicionário com um cadastro válido |
| `inactive_seller` | Seller status `Inativo`, código `'1234'` |
| `active_seller` | Seller status `Ativo` |
| `product` | Produto de exemplo do seller 1 |

Você pode criar outras fixtures se precisar.

---

# 📋 FLUXO 1 — Cadastro de Seller

**Arquivo a criar:** `tests/test_seller_service_create.py`
**Método sob teste:** `SellerService.create_seller(name, cnpj, email, phone, password)`

### Regras implementadas

1. Todos os campos são obrigatórios
2. CNPJ precisa ser válido (dígitos verificadores), aceita com ou sem máscara
3. E-mail precisa ter formato válido
4. Celular precisa estar no formato `+55DDNNNNNNNNN`
5. Senha precisa ter no mínimo 6 caracteres
6. CNPJ, e-mail e celular são **únicos** → `ConflictError`
7. O CNPJ é salvo **sem máscara** e o e-mail em **minúsculas**
8. A senha **nunca** é salva em texto puro
9. O seller nasce com status **`Inativo`** e um código de ativação de 4 dígitos
10. O código é enviado por WhatsApp/SMS logo após salvar
11. Se o envio falhar, o erro `NotificationError` sobe para quem chamou

### ✅ Casos de teste obrigatórios

| # | Caso | O que verificar |
|---|---|---|
| 1.1 | Cadastro válido | Retorna domínio com `status == 'Inativo'` e os dados corretos |
| 1.2 | Cadastro válido | `repository.save` foi chamado **uma vez** |
| 1.3 | Cadastro válido | A senha salva é **diferente** de `'123456'` (foi hasheada) |
| 1.4 | Cadastro válido | CNPJ salvo sem máscara e e-mail em minúsculas |
| 1.5 | Cadastro válido | `notifier.send_activation_code` chamado com **o celular e o código corretos** |
| 1.6 | Nome vazio | Levanta `ValidationError` |
| 1.7 | CNPJ inválido | Levanta `ValidationError` |
| 1.8 | E-mail inválido | Levanta `ValidationError` |
| 1.9 | Celular fora do formato | Levanta `ValidationError` |
| 1.10 | Senha com menos de 6 caracteres | Levanta `ValidationError` |
| 1.11 | Qualquer entrada inválida | `repository.save` **não** foi chamado |
| 1.12 | E-mail já cadastrado | Levanta `ConflictError` |
| 1.13 | CNPJ já cadastrado | Levanta `ConflictError` |
| 1.14 | Celular já cadastrado | Levanta `ConflictError` |
| 1.15 | Conflito | A mensagem **não** foi enviada |
| 1.16 | Provedor de mensagem falha | `NotificationError` sobe (use `side_effect`) |

---

# 📋 FLUXO 2 — Envio da mensagem (integração externa)

**Arquivo a criar:** `tests/test_whats_app.py`
**Classes sob teste:** `WhatsAppClient` e `ActivationNotifier`

Aqui você **não pode** deixar a requisição sair. Use `patch` no `requests.post`:

```python
with patch('src.Infrastructure.http.whats_app.requests.post') as mock_post:
    ...
```

> 💡 Repare **onde** o patch é aplicado: no módulo **onde o `requests` é usado**,
> e não em `requests.post` direto. Errar isso é o erro clássico de mock.

### ✅ Casos de teste obrigatórios

| # | Caso | O que verificar |
|---|---|---|
| 2.1 | Provedor responde 201 | `send_message` retorna o `sid` do JSON |
| 2.2 | Provedor responde 201 | `requests.post` chamado **uma vez**, com `To`, `From` e `Body` corretos |
| 2.3 | Provedor responde 401/500 | Levanta `NotificationError` |
| 2.4 | `requests` levanta `RequestException` (timeout) | Levanta `NotificationError` |
| 2.5 | `ActivationNotifier` | Monta o texto da mensagem contendo o código e delega ao client |
| 2.6 | `generate_activation_code` | Sempre devolve 4 caracteres numéricos (rode em laço) |
| 2.7 | `generate_activation_code` | Com `random.randint` mockado retornando `7`, o código é `'0007'` |

---

# 📋 FLUXO 3 — Ativação do Seller

**Arquivo a criar:** `tests/test_seller_service_activate.py`
**Método sob teste:** `SellerService.activate_seller(phone, code)`

### Regras implementadas

1. Celular e código são obrigatórios
2. Celular não cadastrado → `NotFoundError`
3. Seller já ativo → `BusinessRuleError`
4. Código diferente do gerado → `ValidationError`
5. Ao ativar: status vira `Ativo` e o `activation_code` é apagado
6. O celular é normalizado antes da busca (`+55 (11) 99999-9999` vira `+5511999999999`)

### ✅ Casos de teste obrigatórios

| # | Caso | O que verificar |
|---|---|---|
| 3.1 | Código correto | Retorna domínio com `status == 'Ativo'` |
| 3.2 | Código correto | `activation_code` do seller virou `None` |
| 3.3 | Código correto | `repository.update` chamado uma vez |
| 3.4 | Código errado | Levanta `ValidationError` e `update` **não** é chamado |
| 3.5 | Celular inexistente | Levanta `NotFoundError` |
| 3.6 | Seller já ativo | Levanta `BusinessRuleError` |
| 3.7 | Celular ou código ausente | Levanta `ValidationError` |
| 3.8 | Celular com máscara | `repository.find_by_phone` é chamado com o número **normalizado** |

---

# 📋 FLUXO 4 — Cadastro de Produto

**Arquivo a criar:** `tests/test_product_service.py`
**Método sob teste:** `ProductService.create_product(seller_id, name, price, quantity, status, img)`

### Regras implementadas

1. Seller precisa existir → `NotFoundError`
2. Seller precisa estar **`Ativo`** → `BusinessRuleError`
3. Nome obrigatório, máximo 100 caracteres
4. Preço numérico e **maior que zero**
5. Quantidade inteira e **maior ou igual a zero**
6. Status só pode ser `'Ativo'` ou `'Inativo'`
7. O mesmo seller não pode ter dois produtos com o mesmo nome → `ConflictError`
8. Status padrão é `'Ativo'`

### ✅ Casos de teste obrigatórios

| # | Caso | O que verificar |
|---|---|---|
| 4.1 | Produto válido, seller ativo | Retorna domínio correto; `product_repository.save` chamado uma vez |
| 4.2 | Produto válido | Status padrão é `'Ativo'` e o `seller_id` está correto |
| 4.3 | Seller inexistente | Levanta `NotFoundError` |
| 4.4 | Seller **inativo** | Levanta `BusinessRuleError` e nada é salvo |
| 4.5 | Nome vazio ou só espaços | Levanta `ValidationError` |
| 4.6 | Nome com mais de 100 caracteres | Levanta `ValidationError` |
| 4.7 | Preço zero ou negativo | Levanta `ValidationError` |
| 4.8 | Preço não numérico (`"dez"`) | Levanta `ValidationError` |
| 4.9 | Quantidade negativa | Levanta `ValidationError` |
| 4.10 | Quantidade decimal (`1.5`) | Levanta `ValidationError` |
| 4.11 | Status inválido (`'Pendente'`) | Levanta `ValidationError` |
| 4.12 | Nome já existe para o seller | Levanta `ConflictError` |
| 4.13 | `list_products` | Retorna a lista convertida em domínio |
| 4.14 | `list_products` com seller inexistente | Levanta `NotFoundError` |

> 💡 Nos casos 4.5 a 4.11, use `@pytest.mark.parametrize` em vez de copiar e colar o mesmo teste.

---

# 📋 FLUXO 5 — Validadores (teste unitário puro, sem mock)

**Arquivo a criar:** `tests/test_validators.py`

Estas funções não têm dependência nenhuma — são o teste unitário mais puro que existe.
Use `@pytest.mark.parametrize`.

| # | Função | Casos |
|---|---|---|
| 5.1 | `is_valid_cnpj` | Válido com máscara, válido sem máscara, dígito verificador errado, menos de 14 dígitos, todos os dígitos iguais (`11111111111111`), `None` |
| 5.2 | `is_valid_email` | Válido, sem `@`, sem domínio, sem TLD, vazio, `None` |
| 5.3 | `is_valid_phone` | Válido com 11 dígitos, válido com 10, sem `+55`, com máscara, com letras |
| 5.4 | `is_valid_password` | 6 caracteres (limite), 5 caracteres, vazia, não-string |
| 5.5 | `normalize_cnpj` / `normalize_phone` | Removem a pontuação corretamente |
| 5.6 | `SellerDomain.matches_code` | Código igual, diferente, `None`, com espaços em volta |
| 5.7 | `SellerDomain.is_active` | `Ativo` → `True`, `Inativo` → `False` |

---

# 📝 Exemplo resolvido

Para você ver o padrão esperado — **Arrange / Act / Assert**:

```python
import pytest

from src.Application.Service.seller_service import SellerService
from src.Domain.exceptions import ConflictError


def test_create_seller_envia_codigo_por_whatsapp(
    seller_repository, notifier, code_generator, seller_payload
):
    """Cadastro válido deve enviar o código gerado para o celular informado."""
    # Arrange
    service = SellerService(
        repository=seller_repository,
        notifier=notifier,
        code_generator=code_generator,
    )

    # Act
    seller = service.create_seller(**seller_payload)

    # Assert
    assert seller.status == 'Inativo'
    notifier.send_activation_code.assert_called_once_with('+5511999999999', '1234')


def test_create_seller_com_email_duplicado_nao_envia_mensagem(
    seller_repository, notifier, code_generator, seller_payload, active_seller
):
    """Se o e-mail já existe, nada é salvo e nenhuma mensagem é enviada."""
    # Arrange
    seller_repository.find_by_email.return_value = active_seller
    service = SellerService(seller_repository, notifier, code_generator)

    # Act / Assert
    with pytest.raises(ConflictError):
        service.create_seller(**seller_payload)

    seller_repository.save.assert_not_called()
    notifier.send_activation_code.assert_not_called()
```

---

## 🎯 O que será avaliado

| Critério | Peso |
|---|---|
| **Cobertura dos casos obrigatórios** (as tabelas acima) | 40% |
| **Uso correto de mocks** — isolamento real, sem banco e sem HTTP | 25% |
| **Qualidade das asserções** — `assert_called_once_with`, `side_effect`, verificar o que **não** foi chamado | 15% |
| **Organização** — nomes descritivos, padrão AAA, `parametrize`, sem repetição | 10% |
| **Cobertura de código** — mínimo **80%** em `src/Application/Service/` e `src/Domain/` | 10% |

### Pontos extras

- 🎁 Teste que **prova um bug** no código de produção (com explicação no docstring)
- 🎁 Teste de **contrato HTTP** dos controllers usando `app.test_client()` com o service mockado
- 🎁 Uso de `pytest-mock` (fixture `mocker`) em vez de `unittest.mock` direto

---

## 📦 Entrega

1. Trabalhe a partir da branch `p1`
2. Crie uma branch com seu nome: `git checkout -b p1-seu-nome`
3. Todos os testes ficam dentro de `tests/`
4. Commit final com o resultado de:
   ```bash
   pytest --cov=src --cov-report=term-missing
   ```
5. `pytest` precisa rodar **verde** e **sem conexão com a internet**

---

## ❌ Erros que zeram o item

- Teste que faz requisição HTTP de verdade
- Teste que grava no banco de dados
- Teste que depende de `random` sem mock (resultado diferente a cada execução)
- Alterar `src/` para fazer o teste passar
- Teste sem nenhum `assert`

**Boa prova! 🚀**
