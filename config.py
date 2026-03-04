# config.py


import os
from sqlalchemy import create_engine

class Config(object):
    SECRET_KEY = "claveSecreta"
    SESSION_COOKIE_SECURE = False   

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://Sarahi:root@localhost/ico801'
    SQLALCHEMY_TRACK_MODIFICATIONS = False