import os
from telegram import Update
from telegram.ext import Application, CommandHandler
from dotenv import load_dotenv

from flask import Flask, request  # нужен для веб-сервера

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # URL, который даст Render

# Telegram-бот
app = Application.builder().token(TELEGRAM_TOKEN).build()

# Команды бота
async def start(update: Update, context):
    await update.message.reply_text("Привет! Я бот на webhook 😎")

async def help_command(update: Update, context):
    await update.message.reply_text("Я работаю на webhook. Всё круто!")

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))

# Flask-сервер
flask_app = Flask(__name__)

@flask_app.route(f"/{TELEGRAM_TOKEN}", methods=["POST"])
def receive_update():
    update = Update.de_json(request.get_json(force=True), app.bot)
    app.update_queue.put_nowait(update)
    return "ok"

# Устанавливаем webhook при запуске
async def set_webhook():
    await app.bot.set_webhook(url=f"{WEBHOOK_URL}/{TELEGRAM_TOKEN}")

# Запускаем всё
if __name__ == "__main__":
    import asyncio
    asyncio.run(set_webhook())  # устанавливаем webhook
    flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
