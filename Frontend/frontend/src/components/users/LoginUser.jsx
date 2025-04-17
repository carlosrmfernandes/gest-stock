import './css/Login.css'

function LoginUser() {
     async function Logado(){
        let api = await fetch("http://127.0.0.1:8000/login",{
          method: 'POST',
          body:JSON.stringify({
            "emial": "teste@email.com",
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
    );
  }   
  
  export default LoginUser