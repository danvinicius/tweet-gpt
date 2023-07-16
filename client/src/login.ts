const login_btn = document.getElementById("login_btn");

const email_login = document.getElementById("email") as HTMLInputElement;
const senha_login = document.getElementById("senha") as HTMLInputElement;
const error_span_login = document.getElementById("error") as HTMLSpanElement;

login_btn?.addEventListener("click", async (event: Event) => {
  event.preventDefault();
  const data: any = await realiza_login(email_login.value, senha_login.value);
  if (data.error) {
    error_span_login.innerText = data.error;
    return;
  }
  localStorage.setItem("token", data.message.token);
  window.location.href = "chat.html";
});

const realiza_login = async (email: string, senha: string) => {
  if (email && senha) {
    try {
      const res = await fetch("http://localhost:5000/usuarios/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
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
  error_span_login.innerText = 'Dados inválidos';
};
