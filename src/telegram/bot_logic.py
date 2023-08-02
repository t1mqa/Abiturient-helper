from databases.db_init import create_user
from dataclasses import dataclass
from src.utils.other_utils import snils_normalize


@dataclass
class TgUser:
    tgId: str
    status: str
    SNILS: str | None
    universities: list[str] | None


def preprocess_message(bot, message):
    user_id = message.from_user.id
    status = None
    # TODO: CHECK USER STATUS
    if status == '' or status is None or status == 'free':
        return True
    match status:
        case "waiting SNILS":
            if len(snils_normalize(message.text)):
                bot.send_message(message.chat.id, f"Принят СНИЛС: {message.text}\n"
                                                  f"Для изменения СНИЛС введите /snils .")
                # TODO: Set new status 'free' and set snils
            else:
                bot.send_message(message.chat.id, f"Введён неправильный СНИЛС.\n"
                                                  f"Вы можете обратиться в поддержку @t1mqa.go, "
                                                  f"или попробовать ещё раз.")

        case _:
            bot.send_message(message.chat.id, "Обратитесь в техническую поддержку: @t1mqa.go")


def handle_start(bot, message):
    bot.send_message(message.chat.id, "Привет!\n"
                                      "Это бот, помогающий отследить вашу позицию в конкурсных "
                                      "списках абитуриентов.\n\n"
                                      "Для начала работы пришлите свой *СНИЛС.*")
    user = TgUser(str(message.from_user.id), "waiting SNILS", "", [])
    create_user(user)  # Bool status returned


def handle_text(bot, message):
    bot.send_message(message.chat.id, f"Эхо: {message.text}")
