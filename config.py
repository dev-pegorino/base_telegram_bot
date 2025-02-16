from dotenv import load_dotenv
from os import environ


load_dotenv()


TG_TOKEN = environ['TG_TOKEN']
DATABASE_URL = environ['DATABASE_URL']