import os
import sys

class BaseConfig(object):
    SECRET_KEY = os.getenv('SECRET_KEY', 'you-will-never-guess')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True

class DevelopmentConfig(BaseConfig):
    DIALECT = 'mysql'
    DRIVER = 'pymysql'
    USERNAME = 'root'
    PASSWORD = 'liseen'
    HOST = '127.0.0.1'
    PORT = '3306'
    DATABASE = 'linktodapp'

    dev_uri = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE)
    SQLALCHEMY_DATABASE_URI = dev_uri

class ProductionConfig(BaseConfig):
    pro_uri = os.getenv('DATABASE_URL')
    SQLALCHEMY_DATABASE_URI = pro_uri


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}