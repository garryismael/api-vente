import os

from flask import Flask
from flask_restful import Api

from src.config.base import DevConfig, TestConfig
from src.config.database import db, migrate

app_config = TestConfig if os.environ.get('WORK_ENV') == 'TEST' else DevConfig
    
app = Flask(__name__)
app.config.from_object(app_config)
api_rest = Api(app)

db.init_app(app)
migrate.init_app(app, db)
