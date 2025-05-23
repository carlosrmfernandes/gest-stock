import React from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import App from "./App.jsx";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import CadastroUser from "./components/users/CadastroUser.jsx";
import LoginUser from "./components/users/LoginUser.jsx";
import VerificarUser from "./components/users/VerificarUser.jsx";
import Items from "./components/users/Items.jsx";

createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/app-page" element={<App />}> </Route>
        <Route path="/items" element={<Items />}> </Route>
        <Route path="/cadastro-user" element={<CadastroUser />}> </Route>
        <Route path="/login-user" element={<LoginUser />}> </Route>
        <Route path="/verificar-user" element={<VerificarUser />} />
      </Routes>
    </BrowserRouter>
  </React.StrictMode>
);
