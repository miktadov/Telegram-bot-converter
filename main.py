import telebot
from telebot import types

import random
from datetime import datetime

from config import TOKEN, hi, currency, help_text
from extensions import Api



if __name__ == "__main__":
    bot = telebot.TeleBot(TOKEN)

    @bot.message_handler(commands=['start'])
    def welcome(message):
        # В комманде /values нет необходимости так как все валюты доступны в меню.
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        for i in currency:
            markup.add(types.KeyboardButton(i))

        bot.send_sticker(
            message.chat.id,
            open('AnimatedSticker.tgs', 'rb'))
        bot.send_message(
            message.chat.id,
            f'{random.choice(hi)} {message.from_user.first_name}. Я <strong>Бот Алексей</strong>, создан что бы помочь тебе с конвертацией валют.\n\nКакую валюту меняем?',
            parse_mode='html', reply_markup=markup)
        print(f"{datetime.now().strftime('%d.%m.%Y %H:%M')} Пользователь {message.from_user.first_name} запустил бота.")


    @bot.message_handler(content_types=['text'])
    def currency_first(message):
        print(f"{datetime.now().strftime('%d.%m.%Y %H:%M')} Пользователь {message.from_user.first_name} на 1-ом этапе.")
        try:
            if message.chat.type == 'private':

                if message.text in currency[:-1]:
                    next_currency = currency.copy()
                    next_currency.pop(currency.index(message.text))

                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    for i in next_currency:
                        markup.add(types.KeyboardButton(i))

                    first_curr = message.text[:3]

                    text = "На что меняем "+first_curr+"?"
                    bot.send_message(message.chat.id, text, reply_markup=markup)

                    bot.register_next_step_handler(message, currency_last, first_curr)


                elif message.text.lower().strip() == 'help':
                    print(
                        f"{datetime.now().strftime('%d.%m.%Y %H:%M')} Пользователь {message.from_user.first_name} ввел help на 1-ом уровне.")
                    bot.send_message(message.chat.id, help_text, parse_mode='html')
                    bot.send_message(message.chat.id, "Сейчас ты на 1 ом этапе. Выбери валюту которую хочешь поменять.")
                else:
                    print(
                        f"{datetime.now().strftime('%d.%m.%Y %H:%M')} Пользователь {message.from_user.first_name} Неизвестная команда на 1-ем уровне.")
                    bot.send_message(message.chat.id, 'Неизвестная комманда. Пожалуйста, выберите валюту из предложенных.\n\nДля справки отправьте "help" или нажмите кнопку "help" в самом низу меню')
                    bot.register_next_step_handler(message, currency_first)
        except Exception as ex:
            bot.send_message(message.chat.id, f'Ошибка на 1-ом уровне:\n{str(ex)}...\n\nНекорректный ввод. Пожалуйста, выберите валюту из предложенных.\n\nДля справки отправьте "help" или нажмите кнопку "help" ')
            bot.register_next_step_handler(message, currency_first)

    def currency_last(message, first_curr):
        try:
            print(f"{datetime.now().strftime('%d.%m.%Y %H:%M')} Пользователь {message.from_user.first_name} на 2-ом уровне.")
            if message.text in currency[:-1]:
                last_curr = message.text[:3]

                markup = types.ReplyKeyboardRemove(selective=True)

                text = "Меняем "+first_curr+" на "+last_curr
                bot.send_message(message.chat.id, text, reply_markup=markup)
                bot.send_message(message.chat.id, "Введите количество "+first_curr)

                bot.register_next_step_handler(message, currency_count, first_curr, last_curr)
            elif message.text.lower().strip() == 'help':
                print(
                    f"{datetime.now().strftime('%d.%m.%Y %H:%M')} Пользователь {message.from_user.first_name} ввел help на 2-ом уровне.")
                bot.send_message(message.chat.id, help_text, parse_mode='html')
                bot.send_message(message.chat.id, "Сейчас ты на 2 ом этапе. Выбери валюту <strong>на</strong> которую хочешь поменять.", parse_mode='html')
                bot.register_next_step_handler(message, currency_last, first_curr)
            else:
                print(
                    f"{datetime.now().strftime('%d.%m.%Y %H:%M')} Пользователь {message.from_user.first_name} Неизвестная команда на 2-ем уровне.")
                bot.send_message(message.chat.id,
                                 'Неизвестная комманда. Пожалуйста, выберите валюту из предложенных.\n\nДля справки отправьте "help" или нажмите кнопку "help" в самом низу меню')
                bot.register_next_step_handler(message, currency_last, first_curr)
        except Exception as ex:
            print(
                f"{datetime.now().strftime('%d.%m.%Y %H:%M')} Пользователь {message.from_user.first_name} Ошибка на 2-ем уровне.")
            bot.send_message(message.chat.id, f'Ошибка на 2-ом уровне:\n{str(ex)}...\n\nНекорректный ввод. Пожалуйста, выберите валюту из предложенных.\n\nДля справки отправьте "help" или нажмите кнопку "help" ')
            bot.register_next_step_handler(message, currency_last, first_curr)


    def currency_count(message, first_curr, last_curr):
        try:
            print(f"{datetime.now().strftime('%d.%m.%Y %H:%M')} Пользователь {message.from_user.first_name} на 3-ем уровне.")
            if message.text.lower().strip() == 'help':
                print(
                    f"{datetime.now().strftime('%d.%m.%Y %H:%M')} Пользователь {message.from_user.first_name} ввел help на 3-ем уровне.")
                bot.send_message(message.chat.id, help_text, parse_mode='html')
                bot.send_message(message.chat.id, "Сейчас ты на 3-ем этапе. Введи количество валюты, которую хочешь поменять.")
                bot.register_next_step_handler(message, currency_count, first_curr, last_curr)
            else:
                count = float(message.text)

                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

                for i in currency:
                    markup.add(types.KeyboardButton(i))

                api = Api()
                price = api.get_price(first_curr, last_curr, count)
                bot.send_message(message.chat.id, f'{count} {first_curr} равны {price} {last_curr}')

                bot.send_message(message.chat.id, "Конвертируйте еще 😊", reply_markup=markup)
                print(
                    f"{datetime.now().strftime('%d.%m.%Y %H:%M')} Пользователь {message.from_user.first_name} Успешно закончил конвертацию.")
                print(f"\t{message.from_user.first_name} сконвертировал {count} {first_curr} в {price} {last_curr}")
        except Exception as ex:
            print(
                f"{datetime.now().strftime('%d.%m.%Y %H:%M')} Пользователь {message.from_user.first_name} Ошибка на 3-ем уровне.")
            bot.send_message(message.chat.id, f'Ошибка на 3-ем уровне:\n{str(ex)}.\n\nНекорректный ввод. Пожалуйста, введите исключительно число или "help" для справки')
            bot.register_next_step_handler(message, currency_count, first_curr, last_curr)

    bot.polling(none_stop=True)

