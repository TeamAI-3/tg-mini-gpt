# bot/bot.py
import os
from dotenv import load_dotenv

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
MINIAPP_URL = os.getenv("MINIAPP_URL", "").strip()

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is missing (set it in env or .env)")
if not MINIAPP_URL:
    raise RuntimeError("MINIAPP_URL is missing (set it in env or .env)")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kb = InlineKeyboardMarkup([[
        InlineKeyboardButton("Открыть MiniGPT", web_app=WebAppInfo(url=MINIAPP_URL))
    ]])
    await update.message.reply_text("Жми кнопку — откроется Mini App:", reply_markup=kb)


def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()


if name == "main":
    main()