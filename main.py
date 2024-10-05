import os
from dotenv import load_dotenv
from flask import Flask, request
from aiogram import Bot, Dispatcher
from aiogram.types import Update

# Загружаем переменные окружения из .env
load_dotenv()

# Получаем токен бота
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("Токен бота не найден!")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Создаем Flask-приложение
app = Flask(__name__)

# Обработчик команды /start
@dp.message_handler(commands=["start"])
async def send_welcome(message):
    await message.answer("Привет! Это бот с вебхуком.")

# Роут для вебхуков Telegram
@app.route(f"/webhook/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(), bot)
    Dispatcher.set_current(dp)
    bot.set_current(bot)
    dp.process_update(update)
    return "OK", 200

# Установка вебхука при запуске
@app.before_first_request
def setup_webhook():
    webhook_url = f"https://{os.getenv('VERCEL_URL')}/webhook/{TOKEN}"
    bot.set_webhook(webhook_url)

if __name__ == "__main__":
    # Запуск Flask-приложения
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
