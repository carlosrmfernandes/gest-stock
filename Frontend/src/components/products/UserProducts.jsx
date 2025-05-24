import React, { useEffect } from "react";
import "./css/UserProducts.css";
import verify from "../../hooks/autenticate";
function StoreProducts() {
  useEffect(() => {
    verify();
  });               /*MODIFICA O Q PRECISAR COLOCA, AQ EH A TELA Q FAZ O CRUD DOS ITENS DE UM USER Q TA LOGADO */  
                    
  return (
    <div>
      <header>
        <h1 className='site-name'>Gest Stock</h1>
        <a href="/store_products">
          <button className="storePrdotos-btn">Produtos</button>
        </a>
      </header>
      <main id="listar-container">
        <h1>Itens</h1>
        <table className="table-class">
          <thead>
            <tr>
              <th>Imagem</th>
              <th>Nome</th>
              <th>Descrição</th>
              <th>Valor</th>
              <th>Quantidade</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Imagem do Produto</td>
              <td>Item 1</td>
              <td>Descrição do item 1</td>
              <td>R$ 10,00</td>
              <td>5</td>        
            </tr>
          </tbody>
        </table>
        <div id="buttons-container">
          <button className="adicionar-btn">Adicionar</button>
          <button className="editar-btn">Editar</button>
          <button className="excluir-btn">Excluir</button>
        </div>
      </main>
    </div>
  );
}

export default StoreProducts;
