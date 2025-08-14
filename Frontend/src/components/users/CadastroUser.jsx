import "./css/Cadastro.css";
import { useState } from "react";
import { useNavigate } from "react-router-dom";

function CadastroUser() {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
    cnpj: "",
    phone: "",
  });

  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  async function Cadastrado(e) {
    e.preventDefault(); 

    try {
      const api = await fetch("http://127.0.0.1:8000/new_user", {
        method: "POST",
        body: JSON.stringify(formData),
        headers: {
          "Content-Type": "application/json",
        },
      });

      const response = await api.json();

      if (api.ok) {
        console.log("✅ Usuário cadastrado:", response);
        navigate("/verificar", { state: { email: formData.email } });
      } else {
        console.log("❌ Erro ao cadastrar:", response);
      }
    } catch (error) {
      console.log("Erro de rede ou servidor:", error);
    }
  }

  return (
    <div id="cadastro-container">
      <h1>Cadastro</h1>
      <form className="cadastro-form" onSubmit={Cadastrado}>
        <label>
          Nome:
          <input
            type="text"
            name="name"
            value={formData.name}
            onChange={handleChange}
          />
        </label>
        <label>
          CNPJ:
          <input
            type="text"
            name="cnpj"
            value={formData.cnpj}
            onChange={handleChange}
          />
        </label>
        <label>
          Email:
          <input
            type="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
          />
        </label>
        <label>
          Celular:
          <input
            type="tel"
            name="phone"
            value={formData.phone}
            onChange={handleChange}
          />
        </label>
        <label>
          Senha:
          <input
            type="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
          />
        </label>
        <button type="submit">Cadastrar-se</button>
      </form>
    </div>
  );
}

export default CadastroUser;
