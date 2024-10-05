# services/openai_service.py
import aiohttp
import os
from dotenv import load_dotenv
import logging
from aiocache import cached, Cache

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Загружаем переменные окружения
load_dotenv()

# Устанавливаем API-ключ OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

@cached(ttl=3600, cache=Cache.MEMORY)
async def translate_text(text: str, target_language: str) -> str:
    """
    Переводит текст на указанный язык с использованием OpenAI GPT.

    :param text: Текст для перевода.
    :param target_language: Целевой язык ('английский' или 'русский').
    :return: Переведённый текст или сообщение об ошибке.
    """
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    # Формируем запрос на перевод
    prompt = f"Переведи это сообщение на {target_language}: {text}"

    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 100,
        "temperature": 0.3,  # Для более точных переводов
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=data) as resp:
                logger.info(f"OpenAI API ответил статусом: {resp.status}")
                if resp.status == 200:
                    response = await resp.json()
                    translated_text = response['choices'][0]['message']['content'].strip()
                    logger.info(f"Получен перевод: {translated_text}")
                    return translated_text
                else:
                    error_text = f"OpenAI API вернул статус код {resp.status}"
                    logger.error(error_text)
                    return f"Произошла ошибка: {error_text}"
    except Exception as e:
        logger.exception(f"Неожиданная ошибка: {e}")
        return f"Произошла ошибка: {str(e)}"
