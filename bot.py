import openai
import telebot
from gtts import gTTS
import os
import re
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env
load_dotenv()

# Получаем ключи из окружения
openai.api_key = os.getenv('OPENAI_API_KEY')
openai.api_base = os.getenv('OPENAI_API_BASE')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Проверка, что все переменные окружения загружены
if not openai.api_key or not openai.api_base or not TELEGRAM_BOT_TOKEN:
    print("Ошибка: Не все переменные окружения загружены. Проверьте файл .env.")
    exit(1)  # Завершаем выполнение программы

# Инициализация бота
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# Функция для получения ответа от OpenAI
def get_openai_response(user_input):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-1106",
            messages=[{"role": "user", "content": user_input}]
        )
        chat_response = response['choices'][0]['message']['content']
        return chat_response
    except Exception as e:
        return f"Произошла ошибка при получении ответа от OpenAI: {e}"

# Функция для озвучивания текста и отправки голосового сообщения
def send_voice_message(chat_id, text):
    try:
        tts = gTTS(text=text, lang='ru', slow=True)  # Используем параметр slow=True для детской интонации
        audio_file = 'response.mp3'
        tts.save(audio_file)
        with open(audio_file, 'rb') as audio:
            bot.send_voice(chat_id, audio)
        os.remove(audio_file)
    except Exception as e:
        bot.send_message(chat_id, f"Произошла ошибка при озвучивании: {e}")

# Функция для получения гороскопа
def get_horoscope(day, month, year):
    query = f"Гороскоп на сегодня для родившихся {day}.{month}.{year}."
    return get_openai_response(query)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот, работающий с OpenAI. Введите вашу дату рождения в формате ДД.ММ.ГГГГ, чтобы получить гороскоп на один день.")

# Обработчик всех остальных сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_input = message.text

    # Проверка, что введена дата в формате ДД.ММ.ГГГГ
    date_pattern = re.compile(r'^\d{2}\.\d{2}\.\d{4}$')
    if date_pattern.match(user_input):
        day, month, year = user_input.split('.')
        chat_response = get_horoscope(day, month, year)
        send_voice_message(message.chat.id, chat_response)
    else:
        # Если введен не правильный формат, отправляем сообщение
        bot.send_message(message.chat.id, "Пожалуйста, введите дату рождения в формате ДД.ММ.ГГГГ")

# Запуск бота
if __name__ == "__main__":
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(f"Ошибка при запуске бота: {e}")
