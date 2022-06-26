import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters import Regexp

from data import config
from bot.nasa_features.inline_mode import inline_respose, picture_of_the_specific_day, message_info


# Створюємо базовий об'єкт бота використовуючи який ми будемо підключатись до Telegram API
bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)  # Створюємо об'єкт який буде обробляти оновлення які надходять

# Реєструємо handlers для різних типів оновлень
dp.register_message_handler(message_info, commands=["info"])
dp.register_inline_handler(picture_of_the_specific_day,
                           Regexp(regexp="[0-9]{4}-[0-9]{2}-[0-9]{2}"))
dp.register_inline_handler(inline_respose)
