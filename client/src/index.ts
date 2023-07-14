const send_button = document.getElementById("send_button");
const message_input = document.getElementById(
  "message_input"
) as HTMLInputElement;
const chat_inner = document.querySelector(".chat__inner");

enum Sender {
  USER,
  TWEET,
  BOT,
}

const scroll_to_bottom = () => {
  if (chat_inner) {
    chat_inner.scrollTop = chat_inner?.scrollHeight;
  }
};

const add_message = (msg: string, sender: Sender) => {
  if (msg.trim().length) {
    const message_container_div = document.createElement("div");
    message_container_div.className = "chat__message__container";

    const message_div = document.createElement("div");
    message_div.className = "message";

    const message_text = document.createElement("p");
    message_text.innerText = msg.trim();

    if (sender == Sender.USER) {
      message_container_div.classList.add("user");
      message_div.classList.add("right");
    }

    message_div.appendChild(message_text);
    message_container_div.appendChild(message_div);
    chat_inner?.appendChild(message_container_div);

    scroll_to_bottom();
  }
};

const add_message_and_clear_input = (msg: string, sender: Sender) => {
  add_message(message_input?.value, Sender.USER);
  message_input.value = "";
  message_input.focus();
};

message_input.addEventListener("keypress", ({ key }) => {
  if (key == "Enter") {
    add_message_and_clear_input(message_input?.value, Sender.USER);
  }
});

send_button?.addEventListener("click", () => {
  add_message_and_clear_input(message_input?.value, Sender.USER);
});
