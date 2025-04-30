import "./css/Login.css";
import { useState } from "react";

function LoginUser() {
  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  async function Logado(e) {
    e.preventDefault();

    try {
      const api = await fetch("http://127.0.0.1:8000/login", {
        method: "POST",
        body: JSON.stringify(formData),
        headers: {
          "Content-Type": "application/json",
        },
      });

      const response = await api.json();

      if (api.ok) {
        console.log("✅ Login realizado:", response);
      } else {
        console.log("❌ Erro no login:", response);
      }
    } catch (error) {
      console.log("Erro de rede:", error);
    }
  }

  return (
    <div id="login-container">
      <h1>Login</h1>
      <form className="login-form" onSubmit={Logado}>
        <label>
          Email:
          <input
            type="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            required
          />
        </label>
        <label>
          Senha:
          <input
            type="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            required
          />
        </label>
        <label>
          <button type="submit">Entrar</button>
        </label>
      </form>
    </div>
  );
}

export default LoginUser;
