# main.py
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Update
from aiogram.dispatcher.router import Router
import aiohttp
from aiohttp import web
from dotenv import load_dotenv
import os
import asyncio

from handlers.chat_handler import router as handlers_router  # Импортируем роутер из handlers.py

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Загрузка переменных окружения
load_dotenv()
API_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Например: https://your-domain.vercel.app/webhook

if not API_TOKEN or not WEBHOOK_URL:
    logger.error("Необходимо установить переменные окружения BOT_TOKEN и WEBHOOK_URL")
    exit(1)

# Инициализируем бота и диспетчер
bot = Bot(token=API_TOKEN)
dp = Dispatcher()
dp.include_router(handlers_router)

async def handle(request):
    if request.method == "POST":
        try:
            data = await request.json()
            update = Update(**data)
            Dispatcher.set_current(dp)
            Bot.set_current(bot)
            await dp.process_update(update)
            return web.Response(status=200)
        except Exception as e:
            logger.exception(f"Ошибка при обработке webhook: {e}")
            return web.Response(status=500)
    else:
        return web.Response(status=405)

async def on_startup(app):
    await bot.set_webhook(WEBHOOK_URL)
    logger.info(f"Webhook установлен на {WEBHOOK_URL}")

async def on_shutdown(app):
    await bot.delete_webhook()
    await bot.session.close()
    logger.info("Webhook удалён и бот остановлен")

def create_app():
    app = web.Application()
    app.router.add_post('/webhook', handle)
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
    return app

if __name__ == '__main__':
    app = create_app()
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=int(os.getenv("PORT", 8000)))
