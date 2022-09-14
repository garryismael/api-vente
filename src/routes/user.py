from flask import Blueprint, jsonify, request
from flask_pydantic import validate
from pydantic import Field
from src.models.user import User
from src.schemas.user import UserBase, UserCreate, UserDb
from src.serializers.user import user_serializer, users_serializer
from src.utils.auth import admin_required

user_bp = Blueprint('user_bp', __name__, url_prefix="/users")

@user_bp.get("/")
@admin_required()
def all_users():
    is_admin = request.args.get('is_admin', False)
    users: list[User] = User.query.filter_by(is_admin=is_admin)
    return users_serializer.jsonify(users)

@user_bp.get("/<id>")
@validate()
@admin_required()
def get_one_user(id:int = Field(..., gt=1)):
    user: User = User.query.filter_by(id=id).first_or_404()
    return UserDb.from_orm(user)

@user_bp.post("/")
@validate()
@admin_required()
def create_user(body: UserCreate):
    user: User = user_serializer.load(data=body.dict())
    user.is_admin = True
    user = user.create()
    return UserDb.from_orm(user)

@user_bp.put("/<int:id>")
@validate()
@admin_required()
def edit_user(id: int, body: UserBase):
    user: User = User.query.filter_by(id=id).first_or_404()
    user.update(body)
    return UserDb.from_orm(user)

@user_bp.delete("/<int:id>")
@validate()
@admin_required()
def delete_user(id: int):
    user: User = User.query.filter_by(id=id).first_or_404()
    user.delete()
    return jsonify(msg="deleted successfully"), 200
