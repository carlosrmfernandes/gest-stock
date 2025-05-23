import './App.css'

function App() {
  return (
    <div className='App'>
      <header>
        <h1 className='site-name'>Gest Stock</h1>
        <div className='app-buttons'>
          <a href="/cadastro-user">
            <button className='btn-cadastro'>Cadastrar</button>
          </a>
          <a href="/login-user">
            <button className='btn-login'>Login</button>
          </a>
        </div>
      </header>
      <main>
        <div>
          <h2>Bem-vindo ao Gest Stock</h2>
          <p>O Gest Stock é um sistema de gestão de estoque que permite controlar e monitorar o inventário de produtos de forma eficiente.</p>
          <p>Com o Gest Stock, você pode cadastrar produtos, gerenciar entradas e saídas de estoque, visualizar e comprar produtos de outros usuarios.</p>
          <p>Experimente agora mesmo e otimize a gestão do seu estoque!</p>
        </div>
        <img id="box-img" src="https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExaXQyaGNoNnFvaGh6cXFoeWJrYnlyc3ZreGY1NWxqbmRlYmZuYTJzYSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9cw/uyd7yTQqMzzqXSM01I/giphy.gif" alt="gif-app-page" />
      </main>
      <footer>
        <p>©Todos os direitos reservados.</p>
        <p>Desenvolvedores: Secco, Jhonny e Mendes</p>
      </footer>
    </div>
  )
}

export default App
