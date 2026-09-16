🧪 Prova P1 — Automação de Testes

Projeto: Gest Stock — Gestão de Estoque para Mini Mercados
Branch: p1
Stack de testes: pytest + unittest.mock

📌 Objetivo

O sistema já está implementado. Nesta prova, a tarefa é desenvolver testes automatizados para o cadastro de produtos.

O método a ser testado é:

ProductService.create_product(
    seller_id,
    name,
    price,
    quantity,
    status=PRODUCT_ATIVO,
    img=None
)

Arquivo a ser criado
tests/test_product_service_create.py


⚠️ Importante: não altere o código de produção localizado em src/.

Caso seja identificado um possível bug no código de produção, crie um teste que demonstre o comportamento incorreto e explique o problema no docstring do teste. Essa identificação pode valer ponto extra.

🏛️ Funcionamento do método

O método create_product está localizado em:

src/Application/Service/product_service.py


O fluxo do método deve:

Verificar se o seller_id existe.

Verificar se o seller está ativo.

Validar o nome do produto.

Validar o preço.

Validar a quantidade.

Validar o status.

Verificar se já existe um produto com o mesmo nome para o seller.

Criar o objeto Product.

Salvar o produto.

Retornar o produto criado.

🔧 Mocks

O método possui duas dependências externas que devem ser mockadas:

SellerRepository

ProductRepository

Essas dependências já estão disponíveis nas fixtures de:

tests/conftest.py


A utilização esperada é:

service = ProductService(
    seller_repository=seller_repository,
    product_repository=product_repository,
)

SellerRepository

É utilizado para consultar o seller informado.

Para simular que o seller não existe:

seller_repository.find_by_id.return_value = None


Para os cenários normais, utilize um seller ativo disponibilizado pelo conftest.py.

ProductRepository

É utilizado para:

verificar produtos duplicados;

salvar o produto.

Para indicar que não existe produto duplicado:

product_repository.find_by_name_and_seller.return_value = None


Para indicar que já existe um produto:

product_repository.find_by_name_and_seller.return_value = existing_product

📋 Testes obrigatórios

Os testes devem cobrir as seguintes regras do create_product.

1. Cadastro válido

Um produto com dados válidos deve ser criado com sucesso.

Verifique que:

o produto foi salvo;

o produto criado foi retornado pelo método.

2. Seller inexistente

Quando o seller_id não existir, deve ocorrer:

NotFoundError


O produto não deve ser salvo.

3. Seller inativo

Quando o seller estiver inativo, deve ocorrer:

BusinessRuleError


O produto não deve ser salvo.

4. Nome obrigatório

Um nome vazio deve gerar:

ValidationError


Exemplo:

name=""

5. Nome contendo apenas espaços

Um nome contendo somente espaços deve gerar:

ValidationError


Exemplo:

name="   "

6. Nome maior que 100 caracteres

Um nome com 101 caracteres deve gerar:

ValidationError


Exemplo:

name="A" * 101

7. Nome tratado com strip()

Ao informar:

name="  Arroz  "


o produto salvo deve possuir:

product_salvo.name == "Arroz"

8. Preço não numérico

Um preço não numérico deve gerar:

ValidationError


Exemplo:

price="10.50"

9. Preço menor ou igual a zero

Os valores abaixo devem gerar:

ValidationError

price=0

price=-10

10. Quantidade não inteira

Os exemplos abaixo devem gerar:

ValidationError

quantity=1.5

quantity="10"

11. Quantidade negativa

Uma quantidade negativa deve gerar:

ValidationError


Exemplo:

quantity=-1


A quantidade 0 deve ser considerada válida.

12. Status inválido

O status somente pode ser:

PRODUCT_ATIVO


ou:

PRODUCT_INATIVO


Qualquer outro valor deve gerar:

ValidationError

13. Produto duplicado

O mesmo seller não pode possuir dois produtos com o mesmo nome.

Simule um produto existente:

product_repository.find_by_name_and_seller.return_value = existing_product


Deve ocorrer:

ConflictError


O produto não deve ser salvo.

14. Produto salvo com os dados corretos

Utilize call_args para recuperar o objeto enviado ao save:

product_salvo = product_repository.save.call_args[0][0]


Verifique os seguintes dados:

assert product_salvo.seller_id == seller_id
assert product_salvo.name == "Arroz"
assert product_salvo.price == 10.0
assert product_salvo.quantity == 5
assert product_salvo.status == PRODUCT_ATIVO

15. Preço convertido para float

Ao informar:

price=10


o produto salvo deve possuir:

product_salvo.price == 10.0

16. Imagem e retorno

Ao informar:

img="arroz.jpg"


o produto salvo deve manter:

product_salvo.img == "arroz.jpg"


Além disso, o método deve retornar o produto criado.

🔍 Verificação dos mocks
Verificar se o produto foi salvo
product_repository.save.assert_called_once()

Verificar se o produto não foi salvo
product_repository.save.assert_not_called()

Verificar a consulta do seller
seller_repository.find_by_id.assert_called_once_with(seller_id)

Verificar a consulta de duplicidade
product_repository.find_by_name_and_seller.assert_called_once_with(
    "Arroz",
    seller_id
)

Inspecionar o produto enviado ao save
product_salvo = product_repository.save.call_args[0][0]

⚠️ Comportamento esperado nos erros

Nos cenários de erro, não basta verificar apenas a exceção.

Sempre que o fluxo não deveria chegar ao salvamento, verifique também:

product_repository.save.assert_not_called()


O teste deve comprovar tanto:

o erro esperado;

quanto o comportamento esperado do sistema após o erro.

⭐ Ponto extra — Identificação de Bug

Caso seja encontrado um comportamento incorreto no código de produção:

Não altere src/.

Crie um teste que demonstre o problema e explique o comportamento esperado no docstring.

Exemplo:

def test_algum_comportamento():
    """
    Este teste demonstra um possível bug.

    Quando ..., o método deveria ...
    Porém, atualmente ...
    """

🚀 Executando os testes

Para executar todos os testes:

pytest


Para verificar a cobertura do serviço:

pytest --cov=src.Application.Service.product_service --cov-report=term-missing

✅ Checklist

 Cadastro válido

 Seller inexistente

 Seller inativo

 Nome vazio

 Nome somente com espaços

 Nome acima de 100 caracteres

 strip() do nome

 Preço não numérico

 Preço zero/negativo

 Quantidade não inteira

 Quantidade negativa

 Status inválido

 Produto duplicado

 Dados corretos no save

 Preço convertido para float

 Imagem preservada e produto retornado

📊 Total

16 testes obrigatórios

➕ Ponto extra para identificação e demonstração de um possível bug através de um teste.
