from flask import Blueprint, jsonify, request, send_from_directory
from flask_pydantic import validate
from pydantic import Field
from src.app import app
from src.models.user import User
from src.schemas.user import UserBase, UserCreate, UserDb
from src.serializers.user import user_serializer, users_serializer
from src.utils.auth import admin_required
from src.utils.media import upload_file
from src.utils.form import valid_form
from werkzeug.utils import secure_filename

user_bp = Blueprint('user_bp', __name__, url_prefix="/users")
user_folder = app.config.get('UPLOAD_USER_FOLDER')

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
@valid_form
@validate()
@admin_required()
def create_user():
    data = dict(request.form)
    profile = request.files.get('profile')
    filename = secure_filename(profile.filename)
    body = UserCreate(**data, profile=filename)
    user: User = user_serializer.load(data=body.dict())
    user.is_admin = True
    user = user.create()
    upload_file(profile, user_folder, filename)
    return UserDb.from_orm(user)

@user_bp.put("/<int:id>")
@validate()
@valid_form
@admin_required()
def edit_user(id: int):
    user: User = User.query.filter_by(id=id).first_or_404()
    data = dict(request.form)
    profile = request.files.get('profile')
    filename = user.profile
    if profile is not None:
        filename = secure_filename(profile.filename)
    body = UserBase(**data, profile=filename)
    
    if user.email == body.email:
        user.update(body)
    else:
        other_user = User.query.filter_by(email=body.email).first_or_404()
        if other_user is None:
            user.update(body)
        else:
            return jsonify(email='email must be unique'), 400
    if profile is not None:
        upload_file(profile, user_folder, filename)
        
    return UserDb.from_orm(user)

@user_bp.delete("/<int:id>")
@validate()
@admin_required()
def delete_user(id: int):
    user: User = User.query.filter_by(id=id).first_or_404()
    user.delete()
    return jsonify(msg="deleted successfully"), 200


@user_bp.get("/images/<name>")
def get_image(name: str):
    return send_from_directory(user_folder, name)
