from dotenv import load_dotenv
from os import getenv
from app import App

if __name__ == "__main__":
    load_dotenv()
    token = getenv("TG_APIKEY")
    my_telebot = App(token)
    my_telebot.start()
