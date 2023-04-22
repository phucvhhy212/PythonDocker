import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    USER = os.environ.get('USER')
    PASSWORD = os.environ.get('PASSWORD')
    HOST = os.environ.get('HOST')
    PORT = os.environ.get('PORT')
    DATABASE = os.environ.get('DATABASE')