# 🧪 Prova P1 — Automação de Testes

**Projeto:** Gest Stock — Gestão de Estoque para Mini Mercados
**Branch:** `p1`
**Stack de testes:** `pytest` + `unittest.mock`

---

## 📌 O que você precisa fazer

O sistema **já está implementado**. Sua tarefa é **escrever os testes**.

Você vai testar **um único método**:

```python
SellerService.create_seller(name, cnpj, email, phone, password)
```

É o cadastro de um mini mercado (seller): ele valida os dados, verifica duplicidade,
salva no banco e dispara um código de 4 dígitos por WhatsApp/SMS.

**Arquivo que você deve criar:** `tests/test_seller_service_create.py`

> ⚠️ **Não altere o código de produção** (`src/`). Se você acha que encontrou um bug,
> **escreva um teste que prove o bug** e explique no docstring. Isso vale ponto extra.

> ℹ️ O projeto tem outras funcionalidades (ativação de seller, cadastro de produto).
> **Elas não caem na prova.** Ignore-as.

---

## 🚀 Preparando o ambiente

```bash
git checkout p1

python -m venv .venv
.venv\Scripts\activate         # Windows
source .venv/bin/activate      # Linux/Mac

pip install -r requirements.txt

pytest                                       # roda os testes
pytest --cov=src.Application.Service.seller_service --cov-report=term-missing
```

---

## 🏛️ O que o método faz (leia o código antes de testar)

Abra [`src/Application/Service/seller_service.py`](src/Application/Service/seller_service.py).

O `create_seller` conversa com **três dependências externas**:

```
                    ┌─────────────────────────┐
                    │      SellerService      │
                    │      .create_seller     │
                    └───────────┬─────────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        ▼                       ▼                       ▼
┌──────────────┐      ┌──────────────────┐     ┌──────────────────┐
│SellerReposit.│      │ActivationNotifier│     │generate_activa-  │
│              │      │                  │     │tion_code         │
│ vai no BANCO │      │ vai na INTERNET  │     │ usa RANDOM       │
└──────────────┘      └──────────────────┘     └──────────────────┘
        ▲                       ▲                       ▲
        └───────────────────────┴───────────────────────┘
                     ESTES TRÊS VOCÊ MOCKA
```

As três entram pelo **construtor**. É por isso que dá para mockar sem mágica nenhuma:

```python
service = SellerService(
    repository=seller_repository,       # mock
    notifier=notifier,                  # mock
    code_generator=code_generator,      # mock
)
```

---

# 🔧 OS MOCKS — leia esta seção com atenção

## Regra única, sem exceção

> ### **Todos os 16 testes desta prova usam os 3 mocks. Sempre os três.**

Não existe teste aqui sem mock. Se você escreveu um teste que instancia
`SellerService()` sem argumentos, **ele está errado** — vai tentar abrir o banco
e mandar mensagem de verdade.

## Os 3 mocks

| Dependência real | Por que precisa de mock | Fixture pronta |
|---|---|---|
| `SellerRepository` | Faz `SELECT`/`INSERT` no banco de dados | `seller_repository` |
| `ActivationNotifier` | Faz requisição HTTP para o Twilio (internet) | `notifier` |
| `generate_activation_code` | Usa `random` — o código mudaria a cada execução | `code_generator` |

**Você não precisa criar nenhum deles.** Já estão prontos em
[`tests/conftest.py`](tests/conftest.py) — é só pedir como parâmetro do teste.

## O que cada fixture já vem fazendo

| Fixture | Comportamento padrão |
|---|---|
| `seller_repository` | `find_by_email`, `find_by_cnpj`, `find_by_phone` retornam `None` (banco vazio) e `save` devolve o que recebeu |
| `notifier` | `send_activation_code` funciona e retorna `'SM-fake-sid'` |
| `code_generator` | Sempre retorna a string `'1234'` |
| `seller_payload` | Dicionário com um cadastro **válido**, pronto para `**seller_payload` |
| `active_seller` | Um seller já existente — use para **simular duplicidade** |

Ou seja: **o cenário feliz já vem configurado**. Você só mexe nos mocks quando quer
provocar um erro.

## Como provocar cada cenário

```python
# ❶ Cenário feliz — não configure nada, os defaults já servem
service = SellerService(seller_repository, notifier, code_generator)

# ❷ Simular "e-mail já cadastrado"  (idem para find_by_cnpj / find_by_phone)
seller_repository.find_by_email.return_value = active_seller

# ❸ Simular "o Twilio caiu"
from src.Domain.exceptions import NotificationError
notifier.send_activation_code.side_effect = NotificationError('provedor fora do ar')
```

## Como verificar os mocks depois (isto vale nota)

```python
# Foi chamado exatamente uma vez?
seller_repository.save.assert_called_once()

# Foi chamado com os argumentos certos?
notifier.send_activation_code.assert_called_once_with('+5511999999999', '1234')

# NÃO foi chamado?  (essencial nos testes de erro)
seller_repository.save.assert_not_called()

# Pegar o objeto que foi passado para o mock, para inspecionar os campos
seller_salvo = seller_repository.save.call_args[0][0]
assert seller_salvo.cnpj == '11222333000181'
```

> 💡 O último é o truque mais importante da prova: o `create_seller` monta um objeto
> `Seller` internamente. A única forma de olhar dentro dele é pegando pelo
> `call_args` do mock de `save`.

---

# 📋 Os 16 testes obrigatórios

### Regras que o `create_seller` implementa

1. Todos os campos são obrigatórios
2. CNPJ precisa ser válido (dígitos verificadores), aceita com ou sem máscara
3. E-mail precisa ter formato válido
4. Celular precisa estar no formato `+55DDNNNNNNNNN`
5. Senha precisa ter no mínimo 6 caracteres
6. CNPJ, e-mail e celular são **únicos** → `ConflictError`
7. O CNPJ é salvo **sem máscara** e o e-mail em **minúsculas**
8. A senha **nunca** é salva em texto puro
9. O seller nasce com status **`Inativo`** e um código de ativação de 4 dígitos
10. O código é enviado por WhatsApp/SMS **depois** de salvar
11. Se o envio falhar, o erro `NotificationError` sobe para quem chamou

### Grupo A — Cadastro válido (cenário feliz)

**Mock a configurar: nenhum.** Use as fixtures como vêm.

| # | O que verificar |
|---|---|
| 1.1 | Retorna um domínio com `status == 'Inativo'` |
| 1.2 | `seller_repository.save` foi chamado **uma vez** |
| 1.3 | A senha salva é **diferente** de `'123456'` (foi hasheada) — use `call_args` |
| 1.4 | O CNPJ foi salvo sem máscara e o e-mail em minúsculas — use `call_args` |
| 1.5 | `notifier.send_activation_code` foi chamado com `('+5511999999999', '1234')` |

### Grupo B — Dados inválidos → `ValidationError`

**Mock a configurar: nenhum.** O erro acontece antes de tocar nas dependências.
Em todos, use `with pytest.raises(ValidationError):`.

| # | Entrada inválida |
|---|---|
| 1.6 | Nome vazio |
| 1.7 | CNPJ inválido (ex: `'11.222.333/0001-99'`) |
| 1.8 | E-mail sem `@` |
| 1.9 | Celular fora do formato (ex: `'11999999999'`, sem o `+55`) |
| 1.10 | Senha com 5 caracteres |
| 1.11 | Em **qualquer um** dos casos acima: `save` e `send_activation_code` **não** foram chamados |

> 💡 Faça 1.6 a 1.10 com um único teste usando `@pytest.mark.parametrize`.
> Copiar e colar cinco vezes perde ponto de organização.

### Grupo C — Duplicidade → `ConflictError`

**Mock a configurar:** `seller_repository.find_by_*.return_value = active_seller`

| # | Cenário | O que configurar |
|---|---|---|
| 1.12 | E-mail já cadastrado | `seller_repository.find_by_email.return_value = active_seller` |
| 1.13 | CNPJ já cadastrado | `seller_repository.find_by_cnpj.return_value = active_seller` |
| 1.14 | Celular já cadastrado | `seller_repository.find_by_phone.return_value = active_seller` |
| 1.15 | Em qualquer conflito | `save` **não** foi chamado e a mensagem **não** foi enviada |

### Grupo D — Falha no provedor externo

**Mock a configurar:** `notifier.send_activation_code.side_effect = NotificationError(...)`

| # | O que verificar |
|---|---|
| 1.16 | O `NotificationError` **sobe** para quem chamou (`pytest.raises`), e o seller **já tinha sido salvo** antes da falha (`save.assert_called_once()`) |

---

# 📝 Exemplo resolvido

O padrão esperado — **Arrange / Act / Assert**, com os três mocks sempre presentes:

```python
import pytest

from src.Application.Service.seller_service import SellerService
from src.Domain.exceptions import ConflictError


def test_create_seller_envia_codigo_por_whatsapp(
    seller_repository, notifier, code_generator, seller_payload
):
    """Cadastro válido deve enviar o código gerado para o celular informado."""
    # Arrange — os 3 mocks entram pelo construtor; nada a configurar no cenário feliz
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
    # Arrange — aqui SIM configuramos um mock: o banco "já tem" esse e-mail
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
| **Os 16 casos obrigatórios** cobertos | 40% |
| **Uso correto dos 3 mocks** — nenhum teste toca banco ou internet | 25% |
| **Qualidade das asserções** — `assert_called_once_with`, `call_args`, `side_effect`, e verificar o que **não** foi chamado | 15% |
| **Organização** — nomes descritivos, padrão AAA, `parametrize`, sem repetição | 10% |
| **Cobertura** — o `create_seller` **100% coberto** (veja abaixo como conferir) | 10% |

#### Como conferir sua cobertura

```bash
pytest --cov=src.Application.Service.seller_service --cov-report=term-missing
```

O relatório vai mostrar uma coluna `Missing` com as linhas não cobertas.
O arquivo `seller_service.py` tem **dois** métodos, e só o `create_seller`
(linhas **37 a 94**) cai na prova. O `activate_seller` está fora do escopo.

✅ **Meta:** nenhuma linha entre 37 e 94 aparecendo em `Missing`.
Com os 16 testes feitos, o número total do arquivo fica em torno de **74%** —
isso está **certo**, o que falta é só o `activate_seller`. Não tente cobri-lo.

### Pontos extras

- 🎁 Teste que **prova um bug** no código de produção (com explicação no docstring)
- 🎁 Teste de contrato HTTP do `POST /api/sellers` com `app.test_client()` e o service mockado
- 🎁 Uso de `pytest-mock` (fixture `mocker`) em vez de `unittest.mock` direto

---

## 📦 Entrega

1. Trabalhe a partir da branch `p1`
2. Crie uma branch com seu nome: `git checkout -b p1-seu-nome`
3. Seus testes ficam em `tests/test_seller_service_create.py`
4. Commit final com o resultado de:
   ```bash
   pytest --cov=src.Application.Service.seller_service --cov-report=term-missing
   ```
5. `pytest` precisa rodar **verde** e **sem conexão com a internet**

---

## ❌ Erros que zeram o item

- Instanciar `SellerService()` sem passar os mocks
- Teste que faz requisição HTTP de verdade
- Teste que grava no banco de dados
- Teste que depende de `random` sem mock (resultado diferente a cada execução)
- Alterar `src/` para fazer o teste passar
- Teste sem nenhum `assert`

**Boa prova! 🚀**
