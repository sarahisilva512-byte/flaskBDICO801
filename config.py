import os
from sqlalchemy import create_engine

class Config(object):
    SECRET_KEY = "claveSecreta"
    SESSION_COOCKIE_SECURE = False


class developmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymsql://Sarahi:root@localhost/ico801'
    SQLALCHEMY_TRACK_MODIFICATIONS = False