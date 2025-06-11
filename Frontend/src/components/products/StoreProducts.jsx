import React, { useEffect, useState } from "react";
import "./css/Store.css";
import verify from "../../hooks/autenticate";
import { useNavigate } from "react-router-dom";

function UserProducts() {
  const [products, setProducts] = useState([]);
  const [erro, setErro] = useState("");
  const [mensagem, setMensagem] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    verify();
    fetchProducts();
  }, []);

  const fetchProducts = async () => {
    const token = sessionStorage.getItem("token");

    try {
      const response = await fetch("http://127.0.0.1:8000/list_products", {
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      const data = await response.json();

      if (response.ok) {
        setProducts(data);
      } else {
        setErro(data.erro || "Erro ao buscar produtos");
      }
    } catch (error) {
      setErro("Erro de conexão com o servidor");
      console.error(error);
    }
  };

  const handleComprar = async (productId) => {
    const quantidade = prompt("Digite a quantidade que deseja comprar:");

    if (!quantidade || isNaN(quantidade) || Number(quantidade) <= 0) {
      alert("Quantidade inválida.");
      return;
    }

    const token = sessionStorage.getItem("token");

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/buy_products/${productId}`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({ quantidade: Number(quantidade) }),
        }
      );

      const data = await response.json();

      if (response.ok) {
        setMensagem(data.mensagem);
        fetchProducts(); 
      } else {
        alert(data.erro || "Erro na compra");
      }
    } catch (error) {
      alert("Erro de conexão com o servidor");
      console.error(error);
    }
  };

  const handleCopiar = (item) => {
    navigate("/adicionar-produto", {
      state: {
        name: item.name,
        price: item.price,
        quantity: item.quantity,
        imagem: item.imagem,
      },
    });
  };

  return (
    <div>
      <header>
        <h1 className="site-name">Gest Stock</h1>
        <a href="/user_purchases">
          <button className="meusProdutos-btn">Minhas Compras</button>
        </a>
        <a href="/user_sales">
          <button className="meusProdutos-btn">Minhas Vendas</button>
        </a>
        <a href="/user_products">
          <button className="meusProdutos-btn">Meus Produtos</button>
        </a>
      </header>

      <main id="listar-container">
        <h1>Itens</h1>

        {erro && <p style={{ color: "red" }}>{erro}</p>}
        {mensagem && <p style={{ color: "green" }}>{mensagem}</p>}

        <table className="table-class">
          <thead>
            <tr>
              <th>Vendedor</th>
              <th>Imagem</th>
              <th>Nome</th>
              <th>Descrição</th>
              <th>Valor</th>
              <th>Quantidade</th>
              <th>Ação</th>
            </tr>
          </thead>
          <tbody>
            {products.map((item, index) => (
              <tr key={index}>
                <td>{item.user || "Desconhecido"}</td>
                <td>
                  {item.imagem ? (
                    <img src={item.imagem} alt={item.name} width="60" />
                  ) : (
                    "Sem imagem"
                  )}
                </td>
                <td>{item.name}</td>
                <td>{item.descricao || "Sem descrição"}</td>
                <td>R$ {item.price?.toFixed(2)}</td>
                <td>{item.quantity}</td>
                <td>
                  <button
                    className="comprar-btn"
                    onClick={() => handleComprar(item.id)}
                    disabled={item.quantity === 0}
                  >
                    Comprar
                  </button>
                  <button
                    className="comprar-btn"
                    onClick={() => handleCopiar(item)}
                  >
                    Copiar Produto
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </main>
    </div>
  );
}

export default UserProducts;
