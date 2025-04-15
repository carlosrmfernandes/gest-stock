import './Css/Cadastro.css'

function Cadastro() {
  return (
      <div id="cadastro-container">
        <h2>Cadastro</h2>
          <form className="cadastro-form">
          <label>
            Nome:
            <input type="text" name="nome"/>
          </label>
          <label>
            CNPJ:
            <input type="text" name="cnpj"/>
          </label>
          <label>
            Email:
            <input type="email" name="email"/>
          </label>
          <label>
            Celular:
            <input type="tel" name="celular"/>
          </label>
          <label>
            Senha:
            <input type="password" name="senha"/>
          </label>
          <button type="submit">Cadastrar-se</button>
        </form>
      </div>
  )
}

export default Cadastro
