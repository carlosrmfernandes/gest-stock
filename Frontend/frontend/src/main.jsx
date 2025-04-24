import React from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import { BrowserRouter, Route, Routes } from 'react-router-dom'
import CadastroUser from './components/Users/CadastroUser.jsx'
import LoginUser from './components/Users/LoginUser.jsx'

createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path='/' element={<App/>}></Route>
        <Route path='/cadastro-user' element={<CadastroUser/>}></Route>
        <Route path='/login-user' element={<LoginUser/>}></Route>
      </Routes>
    </BrowserRouter>
  </React.StrictMode>
)
