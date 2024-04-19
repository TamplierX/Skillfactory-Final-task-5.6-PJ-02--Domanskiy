import requests
import json
from config import keys


class APIException(Exception):
    pass


class CurrencyConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        if base == quote:
            raise APIException(f'Вы пытаетесь конвертировать {base} в {base}. \
\nЯ не предназначен для этого. Пожалуйста, введите разные валюты.')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Мне не удалось обработать валюту {base} \
\nЧтобы увидеть список всех доступных валют введите команду /values')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Мне не удалось обработать валюту {quote} \
\nЧтобы увидеть список всех доступных валют введите команду /values')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Мне не удалось обработать количество {amount} \
\nВведите корректное значение.')

        if amount <= 0:
            raise APIException(f'Мне не удалось обработать количество {amount} \
\nВведите корректное значение.')

        r = requests.get(f'https://v6.exchangerate-api.com/v6/348181eb1a9b07e273a79dc5/pair/{base_ticker}/'
                         f'{quote_ticker}')
        final_price = round(json.loads(r.content)['conversion_rate'] * amount, 2)

        return final_price
