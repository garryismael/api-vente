from flask import Blueprint, jsonify
from flask_jwt_extended import create_access_token, jwt_required
from flask_pydantic import validate
from src.models.token import TokenBlocklist
from src.models.user import User
from src.schemas.user import UserCreate, UserDb, UserLogin
from src.serializers.user import UserSerializer, user_serializer
from src.utils.auth import get_authenticated_user

auth_bp = Blueprint('auth_bp', __name__, url_prefix="/auth")

@auth_bp.post("/login")
@validate()
def login(body: UserLogin):
    user: User = User.query.filter_by(email=body.email).first_or_404()
    kwargs = {'identity':body.email}
    kwargs['additional_claims'] = {"is_administrator": True} if user.is_admin else {"is_administrator": False}
    return jsonify(access_token=create_access_token(**kwargs)), 201


@auth_bp.post("/logout")
@jwt_required()
def logout():
    TokenBlocklist.revoke()
    return jsonify(msg="JWT revoked"), 200
    

@auth_bp.post("/register")
@validate()
def register(body: UserCreate):
    user: User = user_serializer.load(data=body.dict())
    user = user.create()
    return UserDb.from_orm(user)

@auth_bp.get('/me')
@jwt_required()
def me():
    user = get_authenticated_user()
    serializer = UserSerializer(only=('id', 'name', 'email', 'address', 'is_admin'))
    return serializer.jsonify(user)
