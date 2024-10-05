import os
import requests
from dotenv import load_dotenv

# Загрузка переменных из файла .env
load_dotenv()

# Получение токена Telegram бота
TOKEN = os.getenv("BOT_TOKEN")

# Формирование URL для вебхука
WEBHOOK_URL = f"https://ai-translator-bot.vercel.app/webhook/{TOKEN}"

# Установка вебхука через Telegram API
response = requests.get(f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={WEBHOOK_URL}")

# Вывод ответа для проверки успешности установки
print(response.json())
