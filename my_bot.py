import telebot
from config import keys, TOKEN
from extensions import ConvertionErrors, Converter

bot = telebot.TeleBot(TOKEN)

# декоратор обработчика команд start, help
@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Для начала работы, введите исходные данные через пробел в формате:\n\
<имя валюты, цену которой нужно узнать>\n<имя валюты, в которой нужно узнать цену первой валюты>\n<количество первой валюты>\n' \
'ПРИМЕР ВВОДА:\nевро доллар 50\n\ncписок доступных валют в формате ввода /valute'
    bot.reply_to(message, text)

# декоратор обработчика команды valute- получение списка доступных валют
@bot.message_handler(commands=['valute'])
def help(message: telebot.types.Message):
    text = 'Список валют:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

# декоратор вывода результата с обработкой исключений
@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise ConvertionErrors('Проверьте количество параметров!')
        quote, base, amount = values
        gen_base = Converter.get_price(quote, base, amount)
    except ConvertionErrors as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f"Цена'{amount} {quote} в {base} - {gen_base}"
        bot.send_message(message.chat.id, text)


bot.polling()
