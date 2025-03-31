import os
from telegram import Update
from telegram.ext import Application, CommandHandler
from dotenv import load_dotenv

# Загружаем токен из .env
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Функция для обработки команды /start
async def start(update: Update, context):
    await update.message.reply_text("Привет! Я твой Telegram-бот 😊")

# Создание бота
app = Application.builder().token(TELEGRAM_TOKEN).build()

# Добавляем команду /start
app.add_handler(CommandHandler("start", start))

# Запускаем бота
if __name__ == "__main__":
    app.run_polling()

