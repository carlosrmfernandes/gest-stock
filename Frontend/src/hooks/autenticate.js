async function verify() {
  try {
    const token = sessionStorage.getItem("token");

    const response = await fetch("http://127.0.0.1:8000/protected", {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
    });

    if (response.ok) {
      console.log("Autenticado com sucesso!");
    } else {
      console.warn("Token inválido. Redirecionando para login...");
      sessionStorage.clear();
      window.location.href = "/login-user";
    }
  } catch (error) {
    console.error("Erro na verificação:", error);
  }
}
export default verify;
