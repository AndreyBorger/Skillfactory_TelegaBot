import requests
import json
from config import keys, APIKEY


# класс собственных исключений
class ConvertionErrors(Exception):
    pass

# класс конвертации с статическим методом обработки исключений и расчетом результата
class Converter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise ConvertionErrors(f'Одинаковые валюты {base}')
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionErrors(f'Неправильно введена валюта {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionErrors(f'Неправильно введена валюта {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionErrors(f'Неправильно введено количество {amount}')

# запрашиваем данные, переводим в json, рассчитываем результат gen_base, поднимаем серверное исключение
        url = f"https://api.apilayer.com/currency_data/live?source={quote_ticker}&currencies={base_ticker}"
        headers = {'apikey': APIKEY}
        res = requests.request("GET", url, headers=headers)
        if res.status_code != 200:
            raise KeyError(f'Закончился лимит запросов API:{res.status_code}')
        res1 = json.loads(res.content)['quotes']
        couple = quote_ticker + base_ticker
        gen_base = round(res1[couple]*amount, 1)
        return gen_base