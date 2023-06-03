import json
import requests
from config import currencies

# обрабтчик ошибок
class APIException(Exception):
    pass

class CurrencyConverter:
    @staticmethod
    # декоратор @staticmethod используется для создания метода, который ничего не знает о классе или экземпляре,
    # через который он был вызван. Он просто получает переданные аргументы,
    # без неявного первого аргумента, и его определение неизменяемо через наследование.
    # метод помогает в достижении инкапсуляции в классе, поскольку он не знает о состоянии текущего экземпляра.

    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise APIException('Вы ввели одинаковые валюты.')

        if quote not in currencies and base not in currencies:
            raise APIException(f'Обе валюты недоступны для бота или не существуют.\nСписок доступных валют: /values')

        try:
           quote_ticker = currencies[quote]
        except KeyError:
            raise APIException(f'Валюта "{quote}" недоступна для бота или не существует.\nСписок доступных валют: /values')

        try:
            base_ticker = currencies[base]
        except KeyError:
            raise APIException(f'Валюта "{base}"  недоступна для бота или не существует.\nСписок доступных валют: /values')

        try:
            amount = float(amount.replace(",", "."))
        except ValueError:
            raise APIException(f'Не удалось обработать количество: "{amount}"')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        price = json.loads(r.content)[currencies[base]]
        total_base = price * float(amount)
        return round(total_base, 3)