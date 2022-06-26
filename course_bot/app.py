import asyncio

from aiogram import executor

from loader import dp

if __name__ == '__main__':
    # Запускаємо бота
    executor.start_polling(dp, skip_updates=True)
