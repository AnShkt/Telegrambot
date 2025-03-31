import os
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler
from dotenv import load_dotenv

# Загружаем токены из .env или Render Environment Variables
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Например: https://твойбот.onrender.com

# Инициализируем Telegram-бота
app = Application.builder().token(TELEGRAM_TOKEN).build()

# Команда /start
async def start(update: Update, context):
    await update.message.reply_text("Привет! Я работаю через Webhook 🔗")

# Команда /help
async def help_command(update: Update, context):
    await update.message.reply_text("Вот что я умею:\n/start — приветствие\n/help — помощь")

# Добавляем команды в приложение
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))

# Flask-сервер
flask_app = Flask(__name__)

# Обработка обновлений от Telegram
@flask_app.route(f"/{TELEGRAM_TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), app.bot)
    app.update_queue.put_nowait(update)
    return "ok", 200

# Установка Webhook
async def set_webhook():
    await app.bot.set_webhook(url=f"{WEBHOOK_URL}/{TELEGRAM_TOKEN}")

# Запуск
if __name__ == "__main__":
    import asyncio
    asyncio.run(set_webhook())
    flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
