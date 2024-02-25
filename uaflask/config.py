import os
from dotenv import load_dotenv

env = os.environ.get
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    SECRET_KEY = env('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg://{env('DB_USER')}:{env('DB_PW')}@{env('DB_HOST')}:{env('DB_PORT')}/{env('DB_DB')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
