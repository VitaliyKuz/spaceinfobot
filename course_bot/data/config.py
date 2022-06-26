import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())  # беремо змінні середовища з файлу .env.

BOT_TOKEN = os.getenv('BOT_TOKEN')  # Токен бота
NASA_TOKEN = os.getenv('NASA_TOKEN')  # Tокен NASA API

