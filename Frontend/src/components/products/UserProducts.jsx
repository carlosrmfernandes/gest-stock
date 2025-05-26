import React, { useEffect, useState } from "react";
import "./css/Store.css";
import verify from "../../hooks/autenticate";

function UserProducts() {
  const [products, setProducts] = useState([]);
  const [erro, setErro] = useState("");
  const [mensagem, setMensagem] = useState("");

  // Estado para controlar o modal de update
  const [showModal, setShowModal] = useState(false);
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [formData, setFormData] = useState({
    name: "",
    price: "",
    quantity: "",
  });
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    verify();
    fetchUserProducts();
  }, []);

  const fetchUserProducts = async () => {
    setErro("");
    const token = sessionStorage.getItem("token");
    const userId = sessionStorage.getItem("user_id");

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/list_user_products/${userId}`,
        {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
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

  const toggleStatus = async (productId) => {
    setErro("");
    const token = sessionStorage.getItem("token");
    try {
      const response = await fetch(
        `http://127.0.0.1:8000/toggle_product_status/${productId}`,
        {
          method: "PATCH",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      const data = await response.json();
      if (response.ok) {
        setMensagem(data.mensagem);
        fetchUserProducts();
      } else {
        setErro(data.erro || "Erro ao alterar status");
      }
    } catch (error) {
      setErro("Erro de conexão com o servidor");
    }
  };

  // Abre modal e preenche form com os dados do produto selecionado
  const openUpdateModal = (product) => {
    setSelectedProduct(product);
    setFormData({
      name: product.name,
      price: product.price,
      quantity: product.quantity,
    });
    setErro("");
    setMensagem("");
    setShowModal(true);
  };

  // Fecha o modal
  const closeModal = () => {
    setShowModal(false);
    setSelectedProduct(null);
    setFormData({ name: "", price: "", quantity: "" });
  };

  // Atualiza os dados do form conforme o usuário digita
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((old) => ({ ...old, [name]: value }));
  };

  // Envia atualização via PUT
  const handleUpdateSubmit = async (e) => {
    e.preventDefault();
    if (!selectedProduct) return;

    setSaving(true);
    setErro("");
    setMensagem("");
    const token = sessionStorage.getItem("token");

    // Validação simples
    if (!formData.name || !formData.price || !formData.quantity) {
      setErro("Preencha todos os campos");
      setSaving(false);
      return;
    }

    // Monta payload com dados corretos (converte price e quantity para número)
    const updatedData = {
      name: formData.name,
      price: parseFloat(formData.price),
      quantity: parseInt(formData.quantity, 10),
    };

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/update_products/${selectedProduct.id}`,
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify(updatedData),
        }
      );
      const data = await response.json();
      if (response.ok) {
        setMensagem(data.mensagem || "Produto atualizado com sucesso");
        fetchUserProducts();
        closeModal();
      } else {
        setErro(data.erro || "Erro ao atualizar produto");
      }
    } catch (error) {
      setErro("Erro de conexão com o servidor");
    }
    setSaving(false);
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

        <a href="/store_products">
          <button className="meusProdutos-btn">Loja</button>
        </a>
        <a href="/adicionar-produto">
          <button className="meusProdutos-btn">Adicionar Produto</button>
        </a>
      </header>

      <main id="listar-container">
        <h1>Meus Produtos</h1>

        {erro && <p style={{ color: "red" }}>{erro}</p>}
        {mensagem && <p style={{ color: "green" }}>{mensagem}</p>}

        <table className="table-class">
          <thead>
            <tr>
              <th>ID</th>
              <th>Nome</th>
              <th>Preço</th>
              <th>Quantidade</th>
              <th>Status</th>
              <th>Ações</th>
            </tr>
          </thead>
          <tbody>
            {products.length > 0 ? (
              products.map((product) => (
                <tr key={product.id}>
                  <td>{product.id}</td>
                  <td>{product.name}</td>
                  <td>R$ {product.price?.toFixed(2)}</td>
                  <td>{product.quantity}</td>
                  <td>{product.status ? "Ativo" : "Inativo"}</td>
                  <td>
                    <button onClick={() => openUpdateModal(product)}>
                      Atualizar
                    </button>
                    <button onClick={() => toggleStatus(product.id)}>
                      {product.status ? "Desativar" : "Ativar"}
                    </button>
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="6">Nenhum produto encontrado.</td>
              </tr>
            )}
          </tbody>
        </table>

        {/* Modal de update */}
        {showModal && (
          <div className="modal-overlay" onClick={closeModal}>
            <div className="modal-content" onClick={(e) => e.stopPropagation()}>
              <h2>Atualizar Produto ID {selectedProduct?.id}</h2>
              {erro && <p style={{ color: "red" }}>{erro}</p>}
              <form onSubmit={handleUpdateSubmit}>
                <label>
                  Nome:
                  <input
                    type="text"
                    name="name"
                    value={formData.name}
                    onChange={handleInputChange}
                  />
                </label>
                <br />
                <label>
                  Preço:
                  <input
                    type="number"
                    step="0.01"
                    name="price"
                    value={formData.price}
                    onChange={handleInputChange}
                  />
                </label>
                <br />
                <label>
                  Quantidade:
                  <input
                    type="number"
                    name="quantity"
                    value={formData.quantity}
                    onChange={handleInputChange}
                  />
                </label>
                <br />
                <div className="modal-actions">
                  <button type="submit" disabled={saving}>
                    {saving ? "Salvando..." : "Salvar"}
                  </button>
                  <button type="button" onClick={closeModal}>
                    Cancelar
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default UserProducts;
