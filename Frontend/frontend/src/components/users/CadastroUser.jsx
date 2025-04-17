import './css/Cadastro.css'

function CadastroUser() {
  function Cadastrado(){
    alert("Cadastro realizado com sucesso!")
  }
  return (
    <div id="cadastro-container">
        <h1>Cadastro</h1>
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
          <button type="submit" onClick={Cadastrado}>Cadastrar-se</button>
        </form>
      </div>
  );
}   

export default CadastroUser