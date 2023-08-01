import telebot


class Bot(telebot.TeleBot):
    def __init__(self, api_key):
        super().__init__(api_key, "MARKDOWN")
        self.register_handlers()

    def register_handlers(self):
        @self.message_handler(commands=['start'])
        def handle_start(message):
            self.send_message(message.chat.id, "Привет!\n"
                                               "Это бот, помогающий отследить вашу позицию в конкурсных "
                                               "списках абитуриентов.\n\n"
                                               "Для начала работы пришлите свой *СНИЛС.*")

        @self.message_handler(content_types=['text'])
        def handle_text(message):
            self.send_message(message.chat.id, f"Эхо: {message.text}")
