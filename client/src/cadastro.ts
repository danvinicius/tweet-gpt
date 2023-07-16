const cadastro_btn = document.getElementById("cadastro_btn");

const nome_cadastro = document.getElementById("nome") as HTMLInputElement;
const email_cadastro = document.getElementById("email") as HTMLInputElement;
const senha_cadastro = document.getElementById("senha") as HTMLInputElement;
const error_span_cadastro = document.getElementById("error") as HTMLSpanElement;

cadastro_btn?.addEventListener("click", async (event: Event) => {
  event.preventDefault();
  const data: any = await realiza_cadastro(
    nome_cadastro.value,
    email_cadastro.value,
    senha_cadastro.value
  );
  if (data.error) {
    error_span_cadastro.innerText = data.error;
    return;
  }
  localStorage.setItem("token", data.message.token);
  window.location.href = "chat.html";
});

const realiza_cadastro = async (nome: string, email: string, senha: string) => {
  if (email && senha && nome) {
    try {
      const res = await fetch("http://localhost:5000/usuarios", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          nome,
          email,
          senha,
        }),
      });
      const data = res.json();
      return data;
    } catch (error) {
      console.log(error);
      return null;
    }
  }
  error_span_cadastro.innerText = "Dados inválidos";
};
