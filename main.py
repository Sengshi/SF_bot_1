import telebot
from extensions import ConverterCurrency, ConvertException
from conf import TOKEN, currency


if __name__ == '__main__':
    bot = telebot.TeleBot(TOKEN)

    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        bot.send_message(message.chat.id, f'Добро пожаловать {message.from_user.first_name}')

    @bot.message_handler(commands=['help'])
    def send_welcome(message):
        bot.send_message(message.chat.id, f'Необходимо ввести <валюта, которую конвертируем> '
                                          f'<валюта, в которую конвертируем> <количество конвертируемой валюты>\n'
                                          f'пример: "доллар рубль 100"')

    @bot.message_handler(commands=['values'])
    def send_welcome(message):
        text = 'Доступные валюты:'
        for i in currency.keys():
            text = '\n'.join((text, i, ))
        bot.send_message(message.chat.id, text)

    @bot.message_handler(content_types=['text'])
    def get_course(message):
        try:
            values = message.text.split()
            if len(values) != 3:
                raise ConvertException('Неверное количество параметров')
            base, quote, amount = values
            response = ConverterCurrency().convert(base, quote, amount)
        except ConvertException as e:
            bot.reply_to(message, f'Ошибка пользователя\n{e}')
        except Exception as e:
            bot.reply_to(message, f'Не удалось обработать команду\n{e}')
        else:
            text = f'{amount} {base} {quote} - {response}'
            bot.send_message(message.chat.id, text)

    bot.polling(none_stop=True)
