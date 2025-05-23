import React, { useEffect } from "react";
import "./css/Listar.css";
import verify from "../../hooks/autenticate";
function ListarProducts() {
  useEffect(() => {
    verify();
  });                     /*MODIFICA O Q PRECISAR*/

  return (
    <div id="listar-container">
      <h1>Itens</h1>
      <table className="table-class">
        <thead>
          <tr>
            <th>Nome</th>
            <th>Descrição</th>
            <th>Valor</th>
            <th>Quantidade</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Item 1</td>
            <td>Descrição do item 1</td>
            <td>R$ 10,00</td>
            <td>5</td>
          </tr>
        </tbody>
      </table>
    </div>
  );
}

export default ListarProducts;
