import datetime
import aiohttp
from data.config import NASA_TOKEN



class NasaApi:
    """ Клас для роботи з Api Nasa. """
    #базова посилання до якого ми будемо додавати параметри та токен
    api_link = f"https://api.nasa.gov/"

    def __init__(self):
        # Початок сесії
        self.session = aiohttp.ClientSession()

        # Базові параметри які будуть відправлені в запиті
        self.params = {'api_key': NASA_TOKEN}

    async def get_picture_of_the_day(self, date=None):
        """ Метод для отримання назви та посилання на картинку дня. """

        #Перевірка введеної дати , якщо дата була введена то в параметри ми додаємо її
        if date:

            self.params.update({'date': date})

        # надсилання запиту до  NASA API
        async with self.session.get(f"{self.api_link}planetary/apod",
                                    params=self.params) as response:
            print("Status: ", response.status)
            # Перетворюємо дані в json формат
            picture_info = await response.json()

            # Закриваємо сесію
            await self.session.close()

            #якщо статус запиту не 200 то помилка
            if response.status != 200:
                raise ValueError(picture_info['msg'])
            print(picture_info)
            return picture_info['title'], picture_info['url']

    async def get_space_forecast(self, for_week=False):
        """ Метод для отримання списку астероїдів для поточного дня або тижня. """
        start_date = datetime.date.today()

        #Якщо прогноз для тижня то кінцева дата буде : поточна + 7 днів
        if for_week:
            end_date = (start_date + datetime.timedelta(days=7))
        # Інакше кінцева дата буде поточним днем
        else:
            end_date = start_date


        self.params.update({'start_date': start_date.isoformat(),
                            'end_date': end_date.isoformat()})
        #надсилаємо запит до API
        async with self.session.get(f"{self.api_link}neo/rest/v1/feed",
                                    params=self.params) as response:
            print("status: ", response.status)
            asteroids = await response.json()
            await self.session.close()
            return asteroids['near_earth_objects']
