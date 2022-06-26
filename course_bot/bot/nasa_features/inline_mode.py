import asyncio  # asyncio — це бібліотека для написання паралельного коду за допомогою синтаксису async/await .

import datetime  # Модуль datetime надає класи для обробки часу та дати різними способами.

# Цей об'єкт представляє повідомлення.
from aiogram.types import Message, InlineQuery, InlineQueryResultPhoto, \
     InlineQueryResultArticle, InputTextMessageContent


from bot.nasa_features.nasa_api import NasaApi


async def picture_of_the_specific_day(query: InlineQuery):
    """ Отримуємо картинку певного дня за його датою. """
    try:
        # перевіряємо правильність дати
        date = datetime.date.fromisoformat(query.query)
        # отримуємо назву та силку на картинку
        title, url = await NasaApi().get_picture_of_the_day(query.query)
    except ValueError:
        result = []  # якщо дата не правильна то ми формуємо пустий результат
    else:
        # формуємо результат з картинкою
        result = [
            InlineQueryResultPhoto(
                id="pic_of_the_day",
                title=f"Picture of the {date.strftime('%d`th %B %Y')}",
                description='For specific day`s picture enter date in format [YYYY-MM-DD]',
                photo_url=url,
                caption=title,
                thumb_url=url
            )
        ]
    # надсилаємо користувачу меню з результатами
    await query.answer(result,
                       cache_time=1,
                       is_personal=True)


async def get_message_for_forecast(for_week=False):
    """ Формуємо повідомлення з прогнозом астероїдів. """
    # отримуємо список небезпечних астероїди
    forecast = await NasaApi().get_space_forecast(for_week)
    message = ""
    print(forecast)
    for day in list(forecast.keys()):
        # розглядаємо кожен окремий день
        for asteroid in forecast[day]:
            # розглядаємо кожен окремий астероїд
            if asteroid['is_potentially_hazardous_asteroid']:
                # якщо астероїд потенційно небезпечний його записуємо

                # визначає параметр астероїда
                min_diameter = float(asteroid['estimated_diameter']['meters']
                                     ['estimated_diameter_min'])
                max_diameter = float(asteroid['estimated_diameter']['meters'][
                                         'estimated_diameter_max'])
                approach_data = asteroid['close_approach_data'][0]
                approach_time = (approach_data['close_approach_date_full'])
                approach_speed = (float(approach_data['relative_velocity']['kilometers_per_hour']))

                # формуємо текст повідомлення
                name_message = f"📰 Object name: {asteroid['name']}"
                diameter_message = (
                    f"📏 Estimated diameter: min={min_diameter:.2f}m, "
                    f"max={max_diameter:.2f}m")
                close_approach_message = (f"🚨 Speed: {approach_speed:.2f}km/h"
                                          f"\n ⌛️Estimated approach time: {approach_time}")

                message = (f"{message}\n{name_message}"
                           f"\n{diameter_message}"
                           f"\n{close_approach_message}"
                           f"\n➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n")
    if len(message) == 0:
        # якщо повідомлення пусте то нічого не знайдено
        message = "Great news, no ☄ found, feel yourself safe."
    else:
        # інакше на початку повідомлення з'являється текст з загрозою
        message = ("Bad news, some potentially hazardous ☄ found. "
                   "Don`t forget to take ☔ "
                   "with you when going outside)"
                   f"\n\n{message}")
    return message


async def get_inline_result():
    """ Формуємо список результатів які будуть відображені в інлайн менюю. """
    title, url = await NasaApi().get_picture_of_the_day()
    result = [
        InlineQueryResultPhoto(
            id="pic_of_the_day",
            title="Picture of the day",
            description='For specific day`s picture enter date in format [YYYY-MM-DD]',
            photo_url=url,
            photo_width=140,
            photo_height=70,
            caption=title,
            thumb_url="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/NASA_logo.svg/255px-NASA_logo.svg.png"
        ),
        InlineQueryResultArticle(
            id="Space_forecast_for_today",
            title="Space forecast for today",
            description='Get the asteroids precipitation forecast🤪',
            input_message_content=InputTextMessageContent(
                await get_message_for_forecast()),
            thumb_url="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/NASA_logo.svg/255px-NASA_logo.svg.png"
        ),
        InlineQueryResultArticle(
            id="Space_forecast_for_week",
            title="Space forecast for week",
            description='Get the asteroids precipitation forecast🤪',
            input_message_content=InputTextMessageContent(
                await get_message_for_forecast(for_week=True)),
            thumb_url="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/NASA_logo.svg/255px-NASA_logo.svg.png"
        )
    ]
    return result


async def inline_respose(query: InlineQuery):
    """ Формуємо інлайн відповідь. """
    print(query)
    result = await get_inline_result()
    await query.answer(result,
                       cache_time=1,
                       is_personal=True)


async def message_info(message: Message):
    """ Надсилаємо інформацію про бота. """
    print(message)
    await message.answer("Для користування бота введіть тег бота. Бот працює в інлайн режимі ;)")