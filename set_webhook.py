import requests
import os
from dotenv import load_dotenv

# Загрузка переменных окружения из файла .env
load_dotenv()

# Получение токена бота
TOKEN = os.getenv("BOT_TOKEN")

# URL для вебхука с использованием домена от Vercel
WEBHOOK_URL = f"https://ai-translator-bot.vercel.app/webhook/{TOKEN}"

# Установка вебхука через Telegram API
response = requests.get(f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={WEBHOOK_URL}")

# Вывод ответа для проверки успешности установки
print(response.json())
