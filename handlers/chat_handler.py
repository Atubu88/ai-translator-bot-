# handlers/chat_handler.py
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from services.openai_service import translate_text
import logging
import re

# Создаём роутер для обработки сообщений
router = Router()

# Настройка логирования
logger = logging.getLogger(__name__)

def is_cyrillic(text: str) -> bool:
    """
    Проверяет, содержит ли текст кириллические символы.
    """
    return bool(re.search('[а-яА-Я]', text))

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "👋 Привет! Я бот-переводчик. Отправь мне текст на русском или английском, и я переведу его для тебя.")

@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer("ℹ️ **Инструкция по использованию бота:**\n\n"
                         "1️⃣ Отправь мне текст на русском или английском языке.\n"
                         "2️⃣ Я автоматически определю язык и переведу текст на противоположный.\n\n"
                         "🛠️ **Пример:**\n"
                         "Пользователь: \"Как дела?\"\n"
                         "Бот: \"How are you?\"\n\n"
                         "Пользователь: \"How are you?\"\n"
                         "Бот: \"Как дела?\"")

@router.message()
async def handle_message(message: Message):
    user_input = message.text.strip()

    if not user_input:
        await message.answer("❌ Пожалуйста, отправьте текст для перевода.")
        return

    try:
        # Определяем язык текста с помощью простой проверки
        if is_cyrillic(user_input):
            target_language = 'английский'
            detected_lang = 'ru'
        else:
            target_language = 'русский'
            detected_lang = 'en'

        logger.info(f"Определён язык: {detected_lang} для текста: {user_input}")

        # Выполняем перевод
        translation = await translate_text(user_input, target_language)

        await message.answer(translation)

    except Exception as e:
        logger.exception(f"Ошибка при обработке сообщения: {e}")
        await message.answer("⚠️ Произошла ошибка при переводе. Пожалуйста, попробуйте позже.")
