import './Css/Login.css'

function Login() {
  return (
    <div id="login-container">
      <h2>Login</h2>
      <form className="login-form">
        <label>
          Email:
          <input type="email" name="email" required/>
        </label>
        <label>
          Senha:
          <input type="password" name="senha" required/>
        </label>
        <label>
          <button type="submit">Entrar</button>
        </label>
      </form>
    </div>
  )
}

export default Login