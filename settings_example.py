import os
import secrets

from dotenv import load_dotenv

load_dotenv()

cwd = os.path.dirname(os.path.realpath(__file__))

HOST = os.environ.get('HOST')
PORT = os.environ.get('PORT')

RADIO_HOST = os.environ.get('RADIO_HOST')
MAIN_RADIO_PORT = os.environ.get('MAIN_RADIO_PORT')

DB_PATH = os.path.join(cwd, 'db.sqlite3')

SECRET = os.environ.get('SECRET', secrets.token_hex(16))

API_SECRET = os.environ.get('API_SECRET')
