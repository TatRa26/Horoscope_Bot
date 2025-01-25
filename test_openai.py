import openai
from dotenv import load_dotenv
import os

# Загрузка переменных из .env
load_dotenv()

# Конфиденциальные данные из .env
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_base = os.getenv("OPENAI_API_BASE")

# Тестовый запрос
try:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Привет, как дела?"}]
    )
    print("OpenAI работает! Ответ:")
    print(response['choices'][0]['message']['content'])
except Exception as e:
    print(f"Ошибка при обращении к OpenAI: {e}")
