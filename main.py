import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
import asyncio

# Загружаем переменные окружения из файла .env
load_dotenv()

# Получаем токен бота
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("Токен бота не найден!")

bot = Bot(token=TOKEN)
dp = Dispatcher()


# Обработчик команды /start
@dp.message_handler(commands=["start"])
async def send_welcome(message: Message):
    await message.answer("Привет! Это бот с вебхуком.")


# Включение вебхуков
async def on_startup(app: web.Application):
    webhook_url = f"https://<твой-домен>.vercel.app/webhook/{TOKEN}"
    await bot.set_webhook(webhook_url)
    print(f"Вебхук установлен: {webhook_url}")


async def on_shutdown(app: web.Application):
    await bot.delete_webhook()
    print("Вебхук удалён")


# Основная функция для запуска веб-сервера
async def main():
    app = web.Application()
    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=f"/webhook/{TOKEN}")

    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
    await site.start()

    print("Бот запущен и готов к приёму вебхуков.")
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
