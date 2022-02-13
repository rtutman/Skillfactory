import telebot
from config import keys, TOKEN
from extensions import ConvertionException, CryptoConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Приветствую тебя кожаный мешок в моем цифровом, информационном пространстве.\
    \nЗдесь ты можешь получить актуальную информацию о курсе и стоимости человеческой валюты.\
    \n\
    \nДля того чтобы начать работу введи команду в формате:\n<название валюты>\
    \n<в какую валюту перевести> <количество переводимой валюты>\
    \n\
    \nПример биткоин доллар 0.35\
    \nЧтобы узнать какие валюты доступны, введи команду /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные человеческие валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('Параметры введены неверно.')

        quote, base, amount = values
        total_base = CryptoConverter.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Danger: человеческая ошибка. \n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не получилось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()