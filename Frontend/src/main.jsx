import React from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import App from "./App.jsx";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import CadastroUser from "./components/users/CadastroUser.jsx";
import LoginUser from "./components/users/LoginUser.jsx";
import VerificarUser from "./components/users/VerificarUser.jsx";
import Products from "./components/products/Products.jsx";
import ListarProducts from "./components/products/ListarProducts.jsx";

createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<App />}> </Route>
        <Route path="/cadastro-user" element={<CadastroUser />}> </Route>
        <Route path="/login-user" element={<LoginUser />}> </Route>
        <Route path="/verificar-user" element={<VerificarUser />}> </Route>
        <Route path="/products" element={<Products />}> </Route>
        <Route path="/listar-products" element={<ListarProducts />}> </Route>
      </Routes>
    </BrowserRouter>
  </React.StrictMode>
);
