import telebot.types
import time

from databases.db_init import (create_user, check_user_status,
                               set_user_status, set_user_snils,
                               check_user_snils, get_all_tg_users)
from dataclasses import dataclass
from src.utils.other_utils import snils_normalize, configure_user_positions_message
from src.universities.uni_data import get_all_universities_positions


@dataclass
class TgUser:
    tgId: str
    status: str
    SNILS: str | None
    universities: list[str] | None


def handle_start(bot, message):
    bot.send_message(message.chat.id, "Привет!\n"
                                      "Это бот, помогающий отследить вашу позицию в конкурсных "
                                      "списках абитуриентов.\n\n"
                                      "Для начала работы пришлите свой СНИЛС.\n"
                                      "*На данный момент бот работает только со списками ГУАПа!*",
                     parse_mode='MARKDOWN')
    user = TgUser(message.chat.id, "waiting SNILS", "", [])
    create_user(user)  # Bool status returned


def handle_callback(callback, bot):
    usr_id = callback.message.chat.id
    match callback.data:
        case "user_positions":
            snils = check_user_snils(usr_id)
            data = get_all_universities_positions(snils)
            message = configure_user_positions_message(data)
            bot.send_message(usr_id, message)
            bot.answer_callback_query(callback.id)
        case "set_snils":
            set_user_status(usr_id, "waiting SNILS")
            bot.send_message(usr_id, "Вы изменяете СНИЛС.\n"
                                     "Пришлите номер документа, или напишите 0 для отмены.")
            bot.answer_callback_query(callback.id)
        case "github":
            bot.send_message(usr_id, "Спасибо, что интересуетесь разработкой.\n\n"
                                     "Автор - Тимофей Мартыненко @t1mqa_go\n\n"
                                     "GitHub проекта - https://github.com/t1mqa/Abiturient-helper\n\n"
                                     "P.S. У тебя есть GitHub?\nТвоя лучшая награда - звезда на мой проект!")
            bot.answer_callback_query(callback.id)
        case _:
            bot.send_message(usr_id, 'Что-то сломалось. Обратитесь в поддержку: @t1mqa_go')
            bot.answer_callback_query(callback.id)


def send_menu(bot, message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    button1 = telebot.types.InlineKeyboardButton("Мои места", callback_data='user_positions')
    button2 = telebot.types.InlineKeyboardButton('Изменить СНИЛС', callback_data='set_snils')
    button3 = telebot.types.InlineKeyboardButton('Исходный код', callback_data='github')
    keyboard.add(button1, button2, button3)

    snils = check_user_snils(message.chat.id)

    bot.send_message(message.chat.id,
                     "Вы находитесь в меню.\n\n"
                     f"Ваш СНИЛС: *{snils}*\n\n"
                     "Для просмотра текущих позиций в списках - нажмите 'Мои места'\n\n"
                     "Для изменения *СНИЛС* нажмите кнопку ниже, и отправьте другой номер документа\n\n"
                     "Для просмотра исходного кода (GitHub) и информации о разработчике нажмите "
                     "'Исходный код'",
                     reply_markup=keyboard,
                     parse_mode="MARKDOWN")


def handle_text(bot, message):
    try:
        status = check_user_status(message.from_user.id)
    except TypeError:
        status = 'free'
        user = TgUser(message.from_user.id, "free", "", [])
        bot.send_message(message.chat.id, "Используйте /start.")
        create_user(user)
    if status == '' or status is None or status == 'free':
        send_menu(bot, message)
        return
    match status:
        case "waiting SNILS":
            if message.text == '0':
                set_user_status(message.chat.id, "free")
                snils = check_user_snils(message.chat.id)
                bot.send_message(message.chat.id, 'Вы отменили изменение СНИЛСа\n'
                                                  f'Текущий СНИЛС: {snils}')
            else:
                if len(snils_normalize(message.text)) == 11:
                    bot.send_message(message.chat.id, f"Принят СНИЛС: {message.text}\n")
                    time.sleep(1)
                    set_user_snils(message.from_user.id, snils_normalize(message.text))
                    send_menu(bot, message)
                    set_user_status(message.from_user.id, "free")
                else:
                    bot.send_message(message.chat.id, f"Введён неправильный СНИЛС.\n"
                                                      f"Отменить операцию - напишите 0\n"
                                                      f"Вы можете обратиться в поддержку @t1mqa_go, "
                                                      f"или попробовать ещё раз.")

        case _:
            bot.send_message(message.chat.id, "Обратитесь в техническую поддержку: @t1mqa_go")


def send_updates(bot):
    users = get_all_tg_users()
    for user in users:
        tg_id, snils = user
        data = get_all_universities_positions(snils)
        message = configure_user_positions_message(data)
        bot.send_message(tg_id, message)
