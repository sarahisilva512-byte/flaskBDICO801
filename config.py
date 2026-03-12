import os 
from sqlalchemy import create_engine  

class Config(object):
    SECRET_KEY ="SILVA0309i"
    SESSION_COOKIE_SECURE = False

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://sarahi:SILVA0309i@localhost/ico801?charset=utf8mb4'
    SQLALCHEMY_TRACK_MODIFICATIONS = False