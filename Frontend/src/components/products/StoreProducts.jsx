import React, { useEffect } from "react";
import "./css/Store.css";
import verify from "../../hooks/autenticate";
function UserProducts() {
  useEffect(() => {
    verify();
  });                     /*MODIFICA O Q PRECISAR COLOCA, AQ EH A TELA Q DA PRA VER OS PRODUTOS DE TDS OS USERS*/

  return (
    <div>
      <header>
        <h1 className='site-name'>Gest Stock</h1>
        <a href="/user_products">
          <button className="meusProdutos-btn">Meus Produtos</button>
        </a>
      </header>
      <main id="listar-container">
        <h1>Itens</h1>
        <table className="table-class">
          <thead>
            <tr>
              <th>Vendedor</th>
              <th>Imagem</th>
              <th>Nome</th>
              <th>Descrição</th>
              <th>Valor</th>
              <th>Quantidade</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Secco</td>
              <td>Imagem do Produto</td>
              <td>Item 2</td>
              <td>Descrição do item 2</td>
              <td>R$ 50,00</td>
              <td>3</td>        
            </tr>
          </tbody>
        </table>
        <button className="comprar-btn">Comprar</button>
      </main>
    </div>
  );
}

export default UserProducts;
