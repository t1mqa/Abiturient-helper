import telebot


class App:
    def __init__(self, token):
        self.token = token
        self.bot = telebot.TeleBot(self.token, parse_mode="MARKDOWN")

    def start(self):
        self.bot.polling()
