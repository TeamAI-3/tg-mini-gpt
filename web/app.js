(function () {
  // ===== UI helpers =====
  function banner(text, bg, border) {
    document.body.insertAdjacentHTML(
      "afterbegin",
      "<div style='padding:10px;margin-bottom:8px;background:" + bg +
      ";border:1px solid " + border + ";font-family:Arial;'>" + text + "</div>"
    );
  }

  function safeText(s) {
    return String(s).replace(/[<>&]/g, (c) => ({ "<":"&lt;", ">":"&gt;", "&":"&amp;" }[c]));
  }

  // Ловим любые JS ошибки прямо на экран
  window.onerror = function (msg, src, line, col) {
    banner(
      "JS ERROR ❌<br>" + safeText(msg) + "<br>" + safeText(src  "") + ":" + (line  "") + ":" + (col  ""),
      "#ffecec",
      "#ff7a7a"
    );
  };

  window.addEventListener("unhandledrejection", function (e) {
    var reason = e && e.reason ? (e.reason.message  String(e.reason)) : "unknown";
    banner("PROMISE ERROR ⚠️<br>" + safeText(reason), "#fff3cd", "#ffe08a");
  });

  // Маяк: app.js реально запустился
  banner("APP.JS LOADED ✅", "#eaffea", "#7ad67a");

  // ===== DOM =====
  var chat = document.getElementById("chat");
  var input = document.getElementById("msg");
  var send = document.getElementById("send");

  if (!chat  !input  !send) {
    banner("DOM ERROR ❌ Не найдены элементы #chat/#msg/#send", "#ffecec", "#ff7a7a");
    return;
  }

  function line(who, text) {
    var p = document.createElement("p");
    p.style.margin = "6px 0";
    p.textContent = who + ": " + text;
    chat.appendChild(p);
    chat.scrollTop = chat.scrollHeight;
  }

  // ===== Telegram WebApp =====
  var tg = null;
  if (window.Telegram && window.Telegram.WebApp) {
    tg = window.Telegram.WebApp;
    try {
      tg.ready();
      tg.expand();
      line("system", "Telegram WebApp найден ✅");
    } catch (e) {
      line("system", "Telegram WebApp есть, но ошибка: " + e.message);
    }
  } else {
    line("system", "Открыто не в Telegram (в браузере initData пустой).");
  }

  // ===== Backend =====
  var BACKEND_URL = "https://tg-mini-gpt.onrender.com";

  function api(text) {
    var initData = tg ? (tg.initData  "") : "";
    return fetch(BACKEND_URL + "/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ initData: initData, text: text })
    }).then(function (r) {
      return r.json().then(function (data) {
        if (!r.ok) {
          var detail = (data && data.detail) ? data.detail : "Request failed";
          throw new Error(detail);
        }
        return data.answer;
      }).catch(function () {
        // если ответ не json
        if (!r.ok) throw new Error("Backend error");
        throw new Error("Bad response");
      });
    });
  }

  function setEnabled(v) {
    send.disabled = !v;
    input.disabled = !v;
    send.style.opacity = v ? "1" : "0.6";
  }

  function onSend() {
    var text = (input.value  "").trim();
    if (!text) return;

    line("you", text);
    input.value = "";
    setEnabled(false);

    api(text).then(function (ans) {
      line("gpt", ans);
      setEnabled(true);
      input.focus();
    }).catch(function (e) {
      line("system", "Ошибка: " + (e && e.message ? e.message : String(e)));
      setEnabled(true);
      input.focus();
    });
  }

  // Надёжные обработчики для Telegram WebView
  send.addEventListener("click", onSend);
  send.addEventListener("touchend", function (e) { e.preventDefault(); onSend(); });
  input.addEventListener("keydown", function (e) {
    if (e.key === "Enter") onSend();
  });

  // Подсказка
  line("system", "Готово. Пиши сообщение 👇");
})();