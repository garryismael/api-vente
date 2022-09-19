
from datetime import timedelta
from os import environ


FLASK_SECRET_KEY = environ.get('FLASK_SECRET_KEY')
JWT_SECRET_KEY = environ.get('JWT_SECRET_KEY')
PG_USER = environ.get('POSTGRES_USER')
PG_USER_PASSWORD = environ.get('POSTGRES_USER_PASSWORD')
PG_HOST = environ.get('POSTGRES_HOST')
PG_DATABASE_NAME = environ.get('POSTGRES_DATABASE_NAME')

class BaseConfig(object):
    DEBUG = True
    TESTING = True
    SECRET_KEY = FLASK_SECRET_KEY
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = JWT_SECRET_KEY
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=30)

class DevConfig(BaseConfig):
    ENV = 'development'
    SQLALCHEMY_DATABASE_URI = f"postgresql://{PG_USER}:{PG_USER_PASSWORD}@{PG_HOST}/{PG_DATABASE_NAME}"

