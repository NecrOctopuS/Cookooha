import os
from environs import Env

env = Env()
env.read_env()

current_path = os.path.dirname(os.path.realpath(__file__))
db_path = "sqlite:///" + current_path + "\\test.db"


class Config:
    DEBUG = True
    SECRET_KEY = env.str('SECRET_KEY', 'my-super-secret-phrase-I-dont-tell-this-to-nobody')
    SQLALCHEMY_DATABASE_URI = env.str("DATABASE_URL", db_path)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RECIPES_PER_MAIN_PAGE = env.int('RECIPES_PER_MAIN_PAGE', 6)
