import telebot
from telebot import types

from config import currencies, TOKEN
from extensions import APIException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)

# обработчики  команд
@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    keyboard = types.ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
    kb = [
         types.KeyboardButton(text="доллар рубль 1"),
         types.KeyboardButton(text="евро рубль 1"),
         types.KeyboardButton(text='евро доллар 1'),
        types.KeyboardButton(text='юань рубль 1')
    ]
    keyboard.add(kb[0], kb[1], kb[2], kb[3])
    text="Введите команду боту в формате: \
         \n<валюта> <в какую валюту конвертировать> " \
         "<количество конвертируемой валюты>\nСписок всех доступных валют:  /values"
    chat_id = message.chat.id
    bot.send_message(chat_id, text, reply_markup=keyboard)
    #bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in currencies.keys():
        text ='\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text',])
def convert(message: telebot.types.Message):
    try:
        values = message.text.lower().split()
        if len(values) != 3:
            raise APIException('Нужно ввести 3 параметра. Инструкция /help')

        quote, base, amount = values
        # quote_ticker, base_ticker = keys[quote], keys[base]
        total_base = CurrencyConverter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка  в команде.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Курс: {currencies[quote]} / {currencies[base]} x {amount}  = {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling()