from src.telegram.bot_init import Bot


class App:
    def __init__(self, token):
        self.token = token
        self.bot = Bot(self.token)

    def start(self):
        self.bot.polling()
