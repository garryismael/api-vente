
import os
from datetime import timedelta

FLASK_SECRET_KEY = os.environ.get('FLASK_SECRET_KEY')
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
PG_USER = os.environ.get('POSTGRES_USER')
PG_USER_PASSWORD = os.environ.get('POSTGRES_USER_PASSWORD')
PG_HOST = os.environ.get('POSTGRES_HOST')
PG_DATABASE_NAME = os.environ.get('POSTGRES_DATABASE_NAME')
UPLOAD_FOLDER = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + "/media"

class BaseConfig(object):
    DEBUG = True
    TESTING = True
    SECRET_KEY = FLASK_SECRET_KEY
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = JWT_SECRET_KEY
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=30)
    UPLOAD_FOLDER = UPLOAD_FOLDER
    MAX_CONTENT_LENGTH = 16 * 1000 * 1000
class DevConfig(BaseConfig):
    ENV = 'development'
    SQLALCHEMY_DATABASE_URI = f"postgresql://{PG_USER}:{PG_USER_PASSWORD}@{PG_HOST}/{PG_DATABASE_NAME}"

