import './css/Login.css'

function LoginUser() {
  async function Logado(){
    let api = await fetch("http://127.0.0.1:8000/login",{
      method: 'POST',
      body:JSON.stringify({
        "email": "teste@email.com",       //aqui a gente vai ter q pegar as infos salvas no bd q passa pelo back e vem pro front
        "password": "123456"
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
    <div id="login-container">
      <h1>Login</h1>
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
          <button type="submit" onClick={Logado}>Entrar</button>
        </label>
      </form>
    </div>
    )
}  

export default LoginUser
