import React, { useEffect, useState } from "react";
import "./css/Store.css";
import verify from "../../hooks/autenticate";

function UserSales() {
  const [sales, setSales] = useState([]);
  const [erro, setErro] = useState("");
  const [mensagem, setMensagem] = useState("");

  useEffect(() => {
    verify();
    fetchSales();
  }, []);

  const fetchSales = async () => {
    const token = sessionStorage.getItem("token");

    try {
      const response = await fetch("http://127.0.0.1:8000/list_user_sales", {
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      const data = await response.json();

      if (response.ok) {
        setSales(data);
      } else {
        setErro(data.erro || "Erro ao buscar vendas");
      }
    } catch (error) {
      setErro("Erro de conexão com o servidor");
      console.error(error);
    }
  };

  return (
    <div>
      <header>
        <h1 className="site-name">Gest Stock</h1>
        <a href="/user_sales">
          <button className="meusProdutos-btn">Minhas Vendas</button>
        </a>
      </header>

      <main id="listar-container">
        <h1>Minhas Vendas</h1>

        {erro && <p style={{ color: "red" }}>{erro}</p>}
        {mensagem && <p style={{ color: "green" }}>{mensagem}</p>}

        <table className="table-class">
          <thead>
            <tr>
              <th>ID da Venda</th>
              <th>Produto</th>
              <th>Quantidade</th>
              <th>Preço</th>
              <th>Data</th>
            </tr>
          </thead>
          <tbody>
            {sales.length > 0 ? (
              sales.map((item, index) => (
                <tr key={index}>
                  <td>{item.id}</td>
                  <td>{item.product_name || item.product_id}</td>
                  <td>{item.quantity}</td>
                  <td>R$ {item.price_at_sale?.toFixed(2)}</td>
                  <td>{new Date(item.sale_date).toLocaleString()}</td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="5">Nenhuma venda registrada.</td>
              </tr>
            )}
          </tbody>
        </table>
      </main>
    </div>
  );
}

export default UserSales;
