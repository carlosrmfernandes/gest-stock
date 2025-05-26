import React, { useState } from "react";
import axios from "axios";

function NewProduct() {
  const [name, setName] = useState("");
  const [price, setPrice] = useState("");
  const [quantity, setQuantity] = useState("");
  const [imagem, setImagem] = useState("");
  const [message, setMessage] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    const token = sessionStorage.getItem("token"); // ajustado aqui
    if (!token) {
      setMessage("Usuário não autenticado.");
      return;
    }

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/new_product",
        {
          name,
          price: parseFloat(price),
          quantity: parseInt(quantity),
          imagem,
        },
        {
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
        }
      );

      setMessage(response.data.mensagem);
      setName("");
      setPrice("");
      setQuantity("");
      setImagem("");
    } catch (error) {
      if (error.response) {
        setMessage(error.response.data.erro);
      } else {
        setMessage("Erro ao enviar o formulário");
      }
    }
  };

  return (
    <div style={{ maxWidth: 400, margin: "auto", padding: 20 }}>
      <h2>Cadastrar Novo Produto</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Nome:</label>
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
        </div>

        <div>
          <label>Preço:</label>
          <input
            type="number"
            step="0.01"
            value={price}
            onChange={(e) => setPrice(e.target.value)}
            required
          />
        </div>

        <div>
          <label>Quantidade:</label>
          <input
            type="number"
            value={quantity}
            onChange={(e) => setQuantity(e.target.value)}
            required
          />
        </div>

        <div>
          <label>Imagem (URL):</label>
          <input
            type="text"
            value={imagem}
            onChange={(e) => setImagem(e.target.value)}
          />
        </div>

        <button type="submit">Cadastrar Produto</button>
      </form>

      {message && <p>{message}</p>}
    </div>
  );
}

export default NewProduct;
