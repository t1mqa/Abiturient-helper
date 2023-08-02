"""
This script is running near main.py

Refreshing all databases every 15 minutes.
"""
import time
from os import getenv

from dotenv import load_dotenv

from src.utils.other_utils import get_data_from_file, get_project_abspath
from databases.db_init import create_spec_table, fill_spec_table
from src.universities.GUAP.guap_spb import GUAP
from src.telegram.bot_init import Bot
from src.telegram.bot_logic import send_updates

if __name__ == '__main__':
    guap = GUAP()
    AVAILABLE_UNIVERSITIES = [guap]

    load_dotenv()
    token = getenv("TG_APIKEY")
    bot = Bot(token)

    while True:
        for uni in AVAILABLE_UNIVERSITIES:
            name = uni.get_code_name()
            specsFile = get_project_abspath() + fr'\src\universities\{name}\specs.py'
            specs: dict = get_data_from_file(specsFile)
            for spec, link in specs.items():
                create_spec_table(f"GUAP_{spec}")
                data = uni.parse_spec_net(link)
                fill_spec_table(f"GUAP_{spec}", data[1])
        current_hour, current_minute = [int(time.strftime("%H")), int(time.strftime("%M"))]
        print(f"Updated at: {current_hour:02d}:{current_minute:02d}")
        send_updates(bot)
        time.sleep(60*15)
