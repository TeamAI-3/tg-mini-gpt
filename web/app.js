document.body.insertAdjacentHTML("afterbegin", "<div style='padding:8px;border:1px solid #ccc;margin-bottom:8px;'>JS LOADED ✅</div>");
const tg = window.Telegram?.WebApp;
const chat = document.getElementById("chat");
const input = document.getElementById("msg");
const send = document.getElementById("send");

function line(who, text){
  const p = document.createElement("p");
  p.textContent = ${who}: ${text};
  chat.appendChild(p);
  chat.scrollTop = chat.scrollHeight;
}

/*
  ⚠️ ВАЖНО
  Пока ОСТАВЬ так.
  Мы заменим этот URL ПОСЛЕ ngrok.
*/
const BACKEND_URL = "https://tg-mini-gpt.onrender.com/";

async function api(text){
  const r = await fetch(${BACKEND_URL}/chat, {
    method: "POST",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify({
      initData: tg.initData,
      text: text
    })
  });

  const data = await r.json();
  if(!r.ok) throw new Error(data?.detail || "Ошибка");
  return data.answer;
}

if(!tg){
  line("system", "Открой это через Telegram (Mini App).");
} else {
  tg.ready();
  tg.expand();
  line("system", "Готово. Пиши сообщение 👇");
}

send.onclick = async () => {
  const text = input.value.trim();
  if(!text) return;

  input.value = "";
  line("you", text);

  try {
    const answer = await api(text);
    line("gpt", answer);
  } catch (e) {
    line("system", "Ошибка: " + e.message);
  }
};