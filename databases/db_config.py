from dotenv import load_dotenv
from os import getenv
load_dotenv()


host = "127.0.0.1"
user = "postgres"
password = getenv("DB_PASSWORD")
db_name = "abitur_helper"
port = 5432
