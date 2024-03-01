import os
import redis
from dotenv import load_dotenv

env = os.environ.get
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    SECRET_KEY = env('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg://{env('RDB_USER')}:{env('RDB_PW')}@{env('RDB_HOST')}:{env('RDB_PORT')}/{env('RDB_DB')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

r = redis.Redis(host=env('CACHE_HOST'), port=env('CACHE_PORT'), password=env('CACHE_PW'), decode_responses=True, db=0, protocol=3)
