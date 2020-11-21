import os

DEBUG = True

SECRET_KEY = os.urandom(24)


HOSTNAME = '127.0.0.1'
PORT     = '3306'
DATABASE = 'final_project'
USERNAME = 'root'
PASSWORD = '770429794'
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI

SQLALCHEMY_TRACK_MODIFICATIONS = True
