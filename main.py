import os
from telegram import Update
from telegram.ext import Application, CommandHandler
from dotenv import load_dotenv

# Загружаем токен из переменных окружения
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Команда /start
async def start(update: Update, context):
    await update.message.reply_text("Привет! Я твой Telegram-бот 😊\nНапиши /help, чтобы узнать, что я умею.")

# Команда /help
async def help_command(update: Update, context):
    await update.message.reply_text(
        "Вот что я умею:\n"
        "/start — начать общение\n"
        "/help — показать это сообщение\n"
        "Скоро будет ещё больше функций! 🚀"
    )

# Создание и настройка бота
app = Application.builder().token(TELEGRAM_TOKEN).build()

# Добавление обработчиков команд
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))

# Запуск
if __name__ == "__main__":
    app.run_polling()
