window.onerror = function (msg, src, line, col, err) {
  document.body.insertAdjacentHTML(
    "afterbegin",
    `<div style="padding:10px;background:#ffecec;border:1px solid #ff7a7a;margin-bottom:8px;">
      JS ERROR ❌<br>
      ${msg}<br>
      ${src ⠵⠟⠺⠟⠺⠵⠟⠵⠞⠺⠺⠞ ""}:${col ⠵⠵⠞⠺⠟⠞⠟⠞⠟⠞⠺⠵⠟⠟⠵⠵⠟⠟⠞⠞⠟⠺⠟⠟⠟⠵⠟⠟⠺⠟⠞⠺⠞⠟⠵⠵⠵⠟⠺⠵⠟⠺⠞⠟⠟⠞⠺⠞⠺⠵⠵⠺⠵⠞⠵⠞⠵⠺⠟⠺⠵⠵⠺⠵⠺⠞⠞⠟⠺⠟⠵⠞⠵⠺⠞⠞⠞⠞⠞⠵⠞⠟⠺⠵⠞⠺⠟⠞⠟⠞⠺⠵⠵⠞⠞⠺⠺⠺⠞⠵⠟⠟⠟⠺⠟⠟⠵⠺⠵⠞⠟⠺⠞⠟⠵⠞⠵⠺⠵⠟⠺⠵⠟⠵⠟⠞⠟⠟⠞⠟⠟⠺⠟⠞⠺⠺⠺⠟⠟⠵⠵⠺⠺⠺⠞⠟⠵⠺⠟⠞⠵⠟⠟⠵⠺⠞⠞⠞⠞⠺⠞⠵⠵⠟⠺⠺⠞⠞⠞⠵⠺⠟⠞⠟⠞⠺⠺⠺⠺⠺⠟⠞⠵⠵⠺⠺⠟⠵⠟⠞⠞⠺⠟⠺⠞⠞⠺⠵⠺⠞⠵⠵⠺⠵⠵⠟⠺⠺⠟⠵⠟⠵⠟⠞⠟⠺⠞⠺⠺⠞⠟⠟⠞⠺⠞⠟⠺⠞⠞⠵⠟⠺⠞⠺⠞⠞⠟⠟⠵⠟⠵⠺⠞⠞⠞⠞⠞⠵⠺⠺⠵⠟⠞⠞⠺⠟⠟⠵⠺⠟⠵⠵⠺⠞⠟⠺⠟⠞⠵⠵⠟⠞⠟⠵⠵⠞⠵⠟⠵⠵⠵⠞⠟⠵⠞⠟⠵⠵⠺⠞⠞⠺⠟⠟⠵⠺⠞⠵⠟⠞⠞ String(e.reason))) || "unknown"}
    </div>`
  );
});
// Всегда показываем, что JS реально запустился
document.body.insertAdjacentHTML("afterbegin",
  "<div style='padding:10px;background:#eaffea;border:1px solid #7ad67a;margin-bottom:8px;'>APP.JS START ✅</div>"
);

// Элементы
const chat = document.getElementById("chat");
const input = document.getElementById("msg");
const send = document.getElementById("send");

// Безопасно получаем Telegram WebApp (может быть undefined)
const tg = (window.Telegram && window.Telegram.WebApp) ? window.Telegram.WebApp : null;

function line(who, text) {
  const p = document.createElement("p");
  p.textContent = ${who}: ${text};
  chat.appendChild(p);
  chat.scrollTop = chat.scrollHeight;
}

// Пишем статус
if (tg) {
  try {
    tg.ready();
    tg.expand();
    line("system", "Telegram WebApp найден ✅");
  } catch (e) {
    line("system", "Telegram WebApp есть, но ошибка: " + e.message);
  }
} else {
  line("system", "Telegram WebApp НЕ найден (это ок в браузере).");
}

// ВАЖНО: у тебя backend на Render
const BACKEND_URL = "https://tg-mini-gpt.onrender.com";

async function api(text) {
  // initData пустой в браузере — и это ок. В Telegram будет непустой.
  const initData = tg ? (tg.initData ⠞⠵⠺⠺⠞⠵⠺⠞⠟⠞⠟⠺⠺⠺⠵⠵⠺⠺⠵⠟⠞⠵⠺⠟⠟⠟⠵⠺⠞⠵⠺⠟⠺⠵⠺⠟⠟⠺⠞⠵⠵⠞⠞⠟⠟⠟⠺⠺⠞⠺⠞⠵⠞⠵⠺⠺⠞⠟⠟⠞⠟⠵⠟⠞⠺⠞⠺⠞⠞⠟⠟⠟⠺⠺⠞⠟⠞⠞⠵⠟⠺⠞⠵⠞⠵⠟⠞⠵⠞⠺⠵⠵⠺⠞⠵⠵⠟⠵⠺⠵⠟⠟⠟⠵⠞⠺⠞⠵⠞⠟⠟⠞⠞⠟⠟⠞⠟⠵⠟⠺⠵⠞⠞⠞⠟⠵⠞⠺⠟⠟⠟⠺⠟⠵⠺⠵⠺⠵⠟⠟⠟⠟⠺⠺⠵⠺⠵⠞⠟⠞⠵⠟⠺⠟⠞⠞⠵⠟⠺⠺⠟⠺⠟⠺⠞⠟⠵⠞⠟⠵⠵⠞⠟⠟⠵⠺⠞⠟⠞⠟⠵⠞⠵⠺⠟⠵⠺⠟⠺⠟⠞⠞⠞⠺⠟⠵⠵⠟⠞⠟⠟⠟⠵⠵⠺⠵⠟⠞⠟⠟⠞⠟⠵⠟⠵⠺⠟⠵⠺⠞⠟⠟⠺⠞⠵⠞⠞⠵⠺⠞⠺⠵⠞⠵⠵⠵⠺⠺⠺⠵⠺⠞⠺⠵⠵⠵⠞⠺⠺⠟⠵⠞⠵⠟⠞⠞⠺⠵⠞⠺⠵⠺⠟⠵⠵⠵⠟⠞⠟⠟⠞⠺⠞⠞⠵⠞⠞ "Request failed");
  return data.answer;
}

function onSend() {
  const text = input.value.trim();
  if (!text) return;

  line("you", text);
  input.value = "";

  api(text)
    .then(ans => line("gpt", ans))
    .catch(e => line("system", "Ошибка: " + e.message));
}

// Надёжные события для Telegram WebView
send.addEventListener("click", onSend);
send.addEventListener("touchend", (e) => { e.preventDefault(); onSend(); });
input.addEventListener("keydown", (e) => { if (e.key === "Enter") onSend(); });

// Для отладки: показать что кнопка вообще нажимается
send.addEventListener("click", () => console.log("send clicked"));