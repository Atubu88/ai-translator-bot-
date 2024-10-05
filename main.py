import os
import asyncio
from dotenv import load_dotenv
from flask import Flask, request
from aiogram import Bot, Dispatcher
from aiogram.types import Update
from handlers.chat_handler import router  # Импортируем роутер

# Загружаем переменные окружения из .env
load_dotenv()

# Получаем токен бота
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("Токен бота не найден!")

# Создаем объект бота
bot = Bot(token=TOKEN)

# Создаем объект диспетчера
dp = Dispatcher()

# Включаем роутер
dp.include_router(router)

# Создаем Flask-приложение
app = Flask(__name__)


# Роут для вебхуков Telegram
@app.route(f"/webhook/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(), bot)
    Dispatcher.set_current(dp)
    bot.set_current(bot)

    # Используем asyncio для вызова асинхронной функции
    asyncio.run(dp.process_update(update))
    return "OK", 200


# Установка вебхука при запуске
@app.before_first_request
def setup_webhook():
    webhook_url = f"https://{os.getenv('VERCEL_URL')}/webhook/{TOKEN}"

    # Устанавливаем вебхук асинхронно
    asyncio.run(bot.set_webhook(webhook_url))


if __name__ == "__main__":
    # Запуск Flask-приложения
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
