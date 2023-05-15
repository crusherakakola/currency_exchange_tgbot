import telebot
import re
import extensions
from security import token

bot = telebot.TeleBot(token)
keys = {
    'доллар': 'usd',
    'евро': 'eur',
    'иена': 'jpy',
    'фунт': 'gbp',
    'рубль': 'rub',
}


@bot.message_handler(commands=['start', 'help'])
def manual(message):
    bot.send_message(message.chat.id, f"Чтобы начать работу введите команду "
                                      f"со следующими параметрами в одну строку через пробел:\n\n"
                                      f"<имя валюты цену которой хотите узнать>\n<имя валюты в которой надо узнать "
                                      f"цену первой валюты>\n<количество первой валюты>\n\n"
                                      f"Например:\nдоллар рубль 1\nusd rub 1")


@bot.message_handler(commands=['values'])
def available_currencies(message):
    text = ''
    for i in keys:
        text = text + f'{i} - {keys.get(i).upper()}\n'
    bot.send_message(message.chat.id, f"Доступные валюты:\n{text}")


@bot.message_handler(content_types=['text'])
def convert(message):
    try:
        try:
            if re.match('^\w* \w* \w*$', message.text):
                base, quote, amount = message.text.split(' ')
                base, quote = base.lower(), quote.lower()
                if base in keys.keys():
                    base = keys.get(base)
                if base not in keys.values():
                    raise extensions.APIException(f'Не удалось обработать валюту: {base}')
                if quote in keys.keys():
                    quote = keys.get(quote)
                if quote not in keys.values():
                    raise extensions.APIException(f'Не удалось обработать валюту: {quote}')
                request = extensions.Request(base, quote, amount)
                if base == quote:
                    raise extensions.APIException(f'Вы ввели одинаковые валюты!')
                if not amount.isdigit():
                    raise extensions.APIException(f'Не удалось обработать количество: {amount}!')
                bot.send_message(message.chat.id,
                                 f"{amount} {base.upper()} в {quote.upper()} составляет - {request.get_price()}")
            else:
                raise extensions.APIException(
                    f'Запрос составлен неправильно!\n\nПример правильного запроса:\nдоллар рубль 1\nusd rub 1')
        except extensions.APIException as e:
            bot.reply_to(message, e)
    except Exception as e:
        bot.send_message(message.chat.id, f'Возникла ошибка на сервере!')


bot.polling(none_stop=True)
