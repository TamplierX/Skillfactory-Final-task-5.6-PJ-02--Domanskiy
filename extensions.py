import requests
import json
from config import keys


#  Класс пользовательского исключения.
class APIException(Exception):
    pass


#  Класс конвертера валют.
class CurrencyConverter:
    #  Метод получает введенные данные от пользователя и проверяет их валидность.
    #  Делаем API запрос с помощью библиотеки request и для парсинга полученного ответа используем библиотеку JSON.
    #  Возвращаем результат конвертации.
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        #  Проверяем корректность данных первой валюты.
        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Мне не удалось обработать валюту {base} \
\nЧтобы увидеть список всех доступных валют введите команду /values')

        #  Проверяем корректность данных второй валюты.
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Мне не удалось обработать валюту {quote} \
\nЧтобы увидеть список всех доступных валют введите команду /values')

        #  Проверяем корректность данных множителя валюты.
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Мне не удалось обработать количество {amount} \
\nВведите корректное значение.')

        #  Нет смысла конвертировать валюту если ее количество ноль или меньше нуля, выводим исключение.
        if amount <= 0:
            raise APIException(f'Мне не удалось обработать количество {amount} \
\nВведите корректное значение.')

        #  Проверяем не пытается ли пользователь конвертировать одинаковые валюты.
        if base_ticker == quote_ticker:
            raise APIException(f'Вы пытаетесь конвертировать {base_ticker} в {base_ticker}. \
\nЯ не предназначен для этого. Пожалуйста, введите разные валюты.')

        #  Делаем API запрос.
        r = requests.get(f'https://v6.exchangerate-api.com/v6/348181eb1a9b07e273a79dc5/pair/{base_ticker}/'
                         f'{quote_ticker}')
        #  Парсим ответ и умножаем его на количество валюты.
        final_price = round(json.loads(r.content)['conversion_rate'] * amount, 2)

        #  Возвращаем результат конвертации.
        return final_price
