import telebot
from src.telegram import bot_logic


class Bot(telebot.TeleBot):
    def __init__(self, api_key):
        super().__init__(api_key, "MARKDOWN")
        self.register_handlers()

    def register_handlers(self):
        self.register_message_handler(lambda message: bot_logic.handle_start(self, message), commands=['start'])
        self.register_message_handler(lambda message: bot_logic.handle_text(self, message), content_types=['text'])



