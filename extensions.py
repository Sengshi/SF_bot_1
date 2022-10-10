import requests
import json
from conf import API_KEY, currency


class ConvertException(Exception):
    pass


class ConverterCurrency:
    @staticmethod
    def convert(base: str, quote: str, amount: str):
        if base == quote:
            raise ConvertException(f'Нельзя конвертировать одну валюту {base}')
        try:
            base_value = currency[base]
        except KeyError:
            raise ConvertException(f'Валюты {base} нет в списке разрешенных')
        try:
            quote_value = currency[quote]
        except KeyError:
            raise ConvertException(f'Валюты {quote} нет в списке разрешенных')
        try:
            amount = float(amount)
        except ValueError:
            raise ConvertException(f'Не удалось обработать количество {amount}')
        params = {
            'from': base_value,
            'to': quote_value,
            'amount': amount,
        }
        headers = {'apikey': API_KEY}
        url = 'https://api.apilayer.com/currency_data/convert'
        response = requests.get(url, params=params, headers=headers)
        res_json = json.loads(response.text)
        return round(res_json['result'], 2)
