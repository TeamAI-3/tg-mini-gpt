from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = "8559402786:AAELAv_WAo80lLTwkvUvDGWa2SeG2injSHY"
MINIAPP_URL = "https://tg-mini-gpt.vercel.app/?v=7777"  # например https://tg-mini-gpt.vercel.app

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kb = InlineKeyboardMarkup([[
        InlineKeyboardButton("Открыть MiniGPT", web_app=WebAppInfo(url=MINIAPP_URL))
    ]])
    await update.message.reply_text("Жми кнопку, откроется Mini App:", reply_markup=kb)

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()

if __name__== "__main__":
    main()