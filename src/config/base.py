import tempfile

DESCRIPTOR, FILE = tempfile.mkstemp(suffix='.sqlite')

class BaseConfig(object):
    DEBUG = True
    TESTING = True
    SECRET_KEY = "my-secret-key"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'jwt-secret-key'


class DevConfig(BaseConfig):
    ENV = 'development'
    SQLALCHEMY_DATABASE_URI = "postgresql://padawan:quelaforcesoitavecvous@localhost/vente"


class TestConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = str.format("sqlite:///{0}", FILE)
