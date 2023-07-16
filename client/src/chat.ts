window.onload = () => {
  const token = localStorage.getItem("token");
  if (!token) {
    window.location.href = "login.html";
    return;
  }
};

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

const logout_button = document.getElementById("logout_button");
const logout = () => {
  localStorage.removeItem("token");
  window.location.href = "login.html";
};
logout_button?.addEventListener("click", (event: Event) => logout());

const scroll_to_bottom = () => {
  if (chat_inner) {
    chat_inner.scrollTop = chat_inner?.scrollHeight;
  }
};

const create_message_container_div = (classes: string[]) => {
  const message_container_div = document.createElement("div");
  message_container_div.classList.add("chat__message__container", ...classes);
  return message_container_div;
};

const create_message_div = () => {
  const message_div = document.createElement("div");
  message_div.classList.add("message");
  return message_div;
};

const create_message_element = (msg: string) => {
  const message_text = document.createElement("p");
  message_text.innerText = msg;
  return message_text;
};

const create_img = (src: string, alt = "", title = "") => {
  const bot_image = document.createElement("img");
  bot_image.src = src;
  bot_image.alt = alt;
  bot_image.title = title;
  return bot_image;
};

const create_twitter_icons_div = () => {
  const twitter_icons_div = document.createElement("div");
  twitter_icons_div.classList.add("message__twitter__icons");
  const comment_img = create_img("./img/comentario.svg");
  const retweet_img = create_img("./img/retweet.svg");
  const curtida_img = create_img("./img/curtida.svg");
  twitter_icons_div.appendChild(comment_img);
  twitter_icons_div.appendChild(retweet_img);
  twitter_icons_div.appendChild(curtida_img);
  return twitter_icons_div;
};

const twitter_user_span = (user: string, date: string) => {
  const user_span = document.createElement("span");
  user_span.classList.add("message__twitter__user");
  user_span.innerText = `@${user} · ${new Date(date).toLocaleDateString(
    "pt-br",
    { day: "numeric", month: "short", year: "numeric" }
  )}`;
  return user_span;
};

const create_bot_message = (msg: string) => {
  const message_container_div = create_message_container_div(["bot", "left"]);
  const message_div = create_message_div();
  const message_text = create_message_element(msg);
  const bot_image = create_img(
    "./img/cabeca-do-bot.svg",
    "Ícone de robô",
    "Tweet GPT"
  );

  message_container_div.appendChild(bot_image);
  message_div.appendChild(message_text);
  message_container_div.appendChild(message_div);
  chat_inner?.appendChild(message_container_div);
};

const create_tweet_message = (
  msg: string,
  twt_user: string,
  twt_date: string
) => {
  const message_container_div = create_message_container_div(["tweet", "left"]);
  const message_div = create_message_div();
  const message_text = create_message_element(msg);
  const twt_image = create_img(
    "./img/logo-do-twitter.svg",
    "Logo do twitter",
    "Twitter"
  );
  const user_span = twitter_user_span(twt_user, twt_date);
  const twitter_icons_div = create_twitter_icons_div();

  message_div.appendChild(user_span);
  message_div.appendChild(message_text);
  message_container_div.appendChild(twt_image);
  message_div.appendChild(twitter_icons_div);
  message_container_div.appendChild(message_div);
  chat_inner?.appendChild(message_container_div);
};

const create_user_message = (msg: string) => {
  const message_container_div = create_message_container_div(["user", "right"]);
  const message_div = create_message_div();
  const message_text = create_message_element(msg);

  message_div.appendChild(message_text);
  message_container_div.appendChild(message_div);
  chat_inner?.appendChild(message_container_div);
};

const add_message = (
  msg: string,
  sender: Sender,
  twt_user = "",
  twt_date = ""
) => {
  if (msg.trim()) {
    if (sender == Sender.USER) {
      create_user_message(msg.trim());
    }
    if (sender == Sender.BOT) {
      create_bot_message(msg.trim());
    }
    if (sender == Sender.TWEET) {
      create_tweet_message(msg.trim(), twt_user, twt_date);
    }
    message_input.value = "";
    message_input.focus();
    scroll_to_bottom();
  }
};

const envia_tag = async (tag: string) => {
  try {
    const token = localStorage.getItem("token");
    if (token) {
      const res = await fetch(
        `http://localhost:5000/search?tag=${tag.replace(/#/, "%23")}`,
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
        }
      );
      const data = res.json();

      return data;
    }
    return null;
  } catch (error) {
    console.log(error);
    return null;
  }
};

message_input.addEventListener("keypress", async ({ key }) => {
  if (key == "Enter") {
    if (message_input?.value.trim()) {
      const tag = (" " + message_input?.value.trim()).slice(1);
      add_message(message_input?.value.trim(), Sender.USER);
      const data = await envia_tag(tag);

      if (data.error) {
        console.log(data.error);
        return;
      }
      add_message(
        data.message.tweet_text,
        Sender.TWEET,
        data.message.user,
        data.message.date
      );
      setTimeout(() => {
        add_message(data.message.analysis, Sender.BOT);
      }, 2000);
    }
  }
});

send_button?.addEventListener("click", async () => {
  if (message_input?.value.trim()) {
    const tag = (" " + message_input?.value.trim()).slice(1);
    add_message(message_input?.value.trim(), Sender.USER);
    const data = await envia_tag(tag);

    if (data.error) {
      console.log(data.error);
      return;
    }
    add_message(
      data.message.tweet_text,
      Sender.TWEET,
      data.message.user,
      data.message.date
    );
    setTimeout(() => {
      add_message(data.message.analysis, Sender.BOT);
    }, 2000);
  }
});
