import 'css/Cadastro.css'

function CadastroUser() {
  async function Cadastrado(){
    let api = await fetch("http://127.0.0.1:8000/new_user",{
      method: 'POST',
      body:JSON.stringify({
        "name": "teste",
        "email": "teste@email.com",     //aqui a gente vai ter q passar as infos pro back q vai mandar pro bd
        "password": "123456",
        "cnpj": "12345678901234",
        "phone": "11987654321",
      }),
      headers:{
        'Content-Type': 'application/json'
      }
    })

    if (api.ok){
      let response = await api.json()
      console.log(response)
    }else{
      let responseError = await api.json()
      console.log(responseError)
    }
  }

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
          <button type="submit" onClick={Cadastrado}>Cadastrar-se</button>
        </form>
      </div>
  );
}   

export default CadastroUser