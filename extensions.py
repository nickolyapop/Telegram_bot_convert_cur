import json
import requests
from config import keys

# обрабтчик ошибок
class ConversationException(Exception):
    pass

class CurrencyConverter:
    @staticmethod
    # декоратор @staticmethod используется для создания метода, который ничего не знает о классе или экземпляре,
    # через который он был вызван. Он просто получает переданные аргументы,
    # без неявного первого аргумента, и его определение неизменяемо через наследование.
    # метод помогает в достижении инкапсуляции в классе, поскольку он не знает о состоянии текущего экземпляра.

    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise ConversationException('Вы ввели одинаковые валюты.')

        if quote not in keys and base not in keys:
            raise ConversationException(f'Обе валюты недоступны для бота или не существуют.\nСписок доступных валют: /values')

        try:
           quote_ticker = keys[quote]
        except KeyError:
            raise ConversationException(f'Валюта "{quote}" недоступна для бота или не существует.\nСписок доступных валют: /values')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConversationException(f'Валюта "{base}"  недоступна для бота или не существует.\nСписок доступных валют: /values')

        try:
            amount = float(amount)
        except ValueError:
            raise ConversationException(f'Не удалось обработать количество: "{amount}"')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]
        return total_base