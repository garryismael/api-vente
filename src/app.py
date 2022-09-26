
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow

from src.config.base import DevConfig
from src.config.database import db, migrate
from src.models.token import TokenBlocklist

app_config = DevConfig
    
app = Flask(__name__)
app.config.from_object(app_config)

db.init_app(app)
migrate.init_app(app, db)
ma = Marshmallow(app)
CORS(app)
jwt = JWTManager(app)

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
    jti = jwt_payload["jti"]
    token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()
    return token is not None

import src.routes.product
import src.routes.auth
import src.routes.purchase
import src.routes.purchase_admin
import src.routes.user