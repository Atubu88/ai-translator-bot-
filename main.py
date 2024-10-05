import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from aiogram import Router
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

# Создаём роутер для регистрации обработчиков
router = Router()

# Обработчик команды /start
@router.message(Command("start"))
async def send_welcome(message: Message):
    await message.answer("Привет! Это бот с вебхуком.")

# Добавляем роутер в диспетчер
dp.include_router(router)

# Включение вебхуков
async def on_startup(app: web.Application):
    webhook_url = f"https://<твой-домен>.vercel.app/webhook/{TOKEN}"
    await bot.set_webhook(webhook_url)
    print(f"Вебхук установлен: {webhook_url}")

async def on_shutdown(app: web.Application):
    await bot.delete_webhook()
    print("Вебхук удалён")

# Основная функция для запуска веб-сервера
# Основная функция для запуска веб-сервера
async def main():
    app = web.Application()  # Создание веб-приложения
    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=f"/webhook/{TOKEN}")

    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
    await site.start()

    print("Бот запущен и готов к приёму вебхуков.")
    await asyncio.Event().wait()

# Экспорт приложения `app` для Vercel
app = web.Application()  # Приложение должно быть доступно как глобальная переменная
SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=f"/webhook/{TOKEN}")
app.on_startup.append(on_startup)
app.on_shutdown.append(on_shutdown)


if __name__ == "__main__":
    asyncio.run(main())
