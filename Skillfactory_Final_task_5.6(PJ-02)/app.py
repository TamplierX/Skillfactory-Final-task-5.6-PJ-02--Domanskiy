import telebot
from config import keys, TOKEN
from extensions import APIException, CurrencyConverter


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def reply_help(message: telebot.types.Message):
    text = ('1. Чтобы конвертировать валюту введите данные (три аргумента написанные через пробел) боту в следующем \
формате:\n<имя валюты, цену которой вы хотите узнать> <имя валюты, в которой надо узнать цену первой валюты> \
<количество первой валюты> \n2. Чтобы увидеть список всех доступных валют введите команду /values')
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты для конвертации: '
    for key in keys.keys():
        text = '\n● '.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values_ = message.text.lower().split(' ')

        if len(values_) != 3:
            raise APIException('Не верный формат данных. Введите данные (три аргумента написанные через пробел) \
боту в следующем формате:\n<имя валюты, цену которой вы хотите узнать> <имя валюты, в которой надо узнать цену первой \
валюты> <количество первой валюты>')

        base, quote, amount = values_
        final_price = CurrencyConverter.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f'Вы допустили ошибку:\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Мне не удалось обработать команду\n{e}')
    else:
        text = f'Если конвертировать {amount} {base} в {quote} получится: {final_price} {quote}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
