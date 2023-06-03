import telebot
from config import keys, TOKEN
from extensions import ConversationException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)

# обработчики  команд
@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text="Введите команду боту в формате: \
         \n<имя валюты> <в какую валюту конвертировать>  \
         <\nколичество конвертируемой валюты>\nСписок всех доступных валют:  /values"
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text ='\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text',])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise ConversationException('Нужно ввести 3 параметра. Инструкция /help')

        quote, base, amount = values
        # quote_ticker, base_ticker = keys[quote], keys[base]
        total_base = CurrencyConverter.get_price(quote, base, amount)
    except ConversationException as e:
        bot.reply_to(message, f'Ошибка пользователся.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Курс: {keys[quote]} / {keys[base]} x {amount}  = {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling()