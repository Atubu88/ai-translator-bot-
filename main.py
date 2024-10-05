# main.py
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Update
from fastapi import FastAPI, Request, Response
from dotenv import load_dotenv
import os
import asyncio
from fastapi.responses import JSONResponse


from handlers.chat_handler import router as handlers_router  # Убедитесь, что путь верен
from services.openai_service import translate_text  # Убедитесь, что путь верен

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Загрузка переменных окружения
load_dotenv()
API_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Например: https://ваш-домен.vercel.app/webhook

if not API_TOKEN or not WEBHOOK_URL:
    logger.error("Необходимо установить переменные окружения BOT_TOKEN и WEBHOOK_URL")
    exit(1)

# Инициализируем бота и диспетчер
bot = Bot(token=API_TOKEN)
dp = Dispatcher()
dp.include_router(handlers_router)

# Создаём FastAPI приложение
app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await bot.set_webhook(WEBHOOK_URL)
    logger.info(f"Webhook установлен на {WEBHOOK_URL}")

@app.on_event("shutdown")
async def on_shutdown():
    await bot.delete_webhook()
    await bot.session.close()
    logger.info("Webhook удалён и бот остановлен")

@app.post("/webhook")
async def webhook_handler(request: Request):
    try:
        data = await request.json()
        update = Update(**data)
        Dispatcher.set_current(dp)
        Bot.set_current(bot)
        await dp.process_update(update)
        return Response(status_code=200)
    except Exception as e:
        logger.exception(f"Ошибка при обработке webhook: {e}")
        return Response(status_code=500)

@app.get("/")
async def root():
    return JSONResponse(content={"message": "Hello, this is the aiogram Telegram bot webhook endpoint."})
