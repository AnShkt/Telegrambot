import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv

# Загружаем токены из .env
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")

# Функция для /start
async def start(update: Update, context):
    await update.message.reply_text("Привет! Я бот для работы с GitHub. Используй /newrepo <имя_репозитория>, чтобы создать новый репозиторий.")

# Функция для создания репозитория
async def create_repo(update: Update, context):
    if not context.args:
        await update.message.reply_text("Введите имя репозитория: /newrepo my-repo")
        return

    repo_name = context.args[0]
    url = f"https://api.github.com/user/repos"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    data = {"name": repo_name, "private": False}

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 201:
        await update.message.reply_text(f"✅ Репозиторий '{repo_name}' создан! \nhttps://github.com/{GITHUB_USERNAME}/{repo_name}")
    else:
        await update.message.reply_text(f"⚠ Ошибка: {response.json().get('message')}")

# Функция для добавления файла
async def add_file(update: Update, context):
    if len(context.args) < 2:
        await update.message.reply_text("Используй: /addfile <repo> <filename> <content>")
        return

    repo_name, file_name, file_content = context.args[0], context.args[1], " ".join(context.args[2:])
    url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{repo_name}/contents/{file_name}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    data = {
        "message": f"Add {file_name}",
        "content": file_content.encode("utf-8").hex(),
        "branch": "main"
    }

    response = requests.put(url, json=data, headers=headers)

    if response.status_code == 201:
        await update.message.reply_text(f"✅ Файл '{file_name}' добавлен в {repo_name}!")
    else:
        await update.message.reply_text(f"⚠ Ошибка: {response.json().get('message')}")

# Создание Telegram-бота
app = Application.builder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("newrepo", create_repo))
app.add_handler(CommandHandler("addfile", add_file))

# Запуск
if __name__ == "__main__":
    app.run_polling()
