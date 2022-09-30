from flask import jsonify, request
from flask_jwt_extended import create_access_token, jwt_required
from flask_pydantic import validate
from src.app import app
from src.models.token import TokenBlocklist
from src.models.user import User
from src.schemas.user import (UserBase, UserCreate, UserDb, UserLogin,
                              UserPassword)
from src.serializers.user import UserSerializer, user_serializer
from src.utils.auth import get_authenticated_user
from src.utils.form import valid_form
from src.utils.media import upload_file
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename

user_folder = app.config.get('UPLOAD_USER_FOLDER')

@app.post("/auth/login")
@validate()
def login(body: UserLogin):
    user: User = User.query.filter_by(email=body.email).first_or_404()
    kwargs = {'identity':body.email}
    kwargs['additional_claims'] = {"is_administrator": True} if user.is_admin else {"is_administrator": False}
    return jsonify(access_token=create_access_token(**kwargs)), 200


@app.post("/auth/logout")
@jwt_required()
def logout():
    TokenBlocklist.revoke()
    return jsonify(msg="JWT revoked"), 200
    

@app.post("/auth/register")
@valid_form
@validate()
def register():
    data = dict(request.form)
    profile = request.files.get('profile')
    filename = secure_filename(profile.filename)
    body = UserCreate(**data, profile=filename)
    user: User = user_serializer.load(data=body.dict())
    user = user.create()
    upload_file(profile, user_folder, filename)
    return UserDb.from_orm(user)

@app.put("/auth/me/edit")
@validate()
@valid_form
@jwt_required()
def edit_me():
    user: User = get_authenticated_user()
    data = dict(request.form)
    if 'profile' in data:
        del data['profile']
    profile = request.files.get('profile')
    filename = user.profile
    if profile is not None and profile.filename != '':
        filename = secure_filename(profile.filename)
    body = UserBase(**data, profile=filename)
    
    if user.email == body.email:
        user.update(body)
    else:
        other_user = User.query.filter_by(email=body.email).first()
        if other_user is None:
            user.update(body)
        else:
            return jsonify(email='email must be unique'), 400
    if profile is not None and profile.filename != '':
        upload_file(profile, user_folder, filename)
        
    return UserDb.from_orm(user)

@app.put("/auth/password/edit")
@validate()
@jwt_required()
def change_my_password(body: UserPassword):
    user: User = get_authenticated_user()
    user.password = generate_password_hash(body.newPassword)
    user.password_changed()
    return jsonify(msg='Password changed'), 200


@app.get('/auth/me')
@jwt_required()
def me():
    user: User = get_authenticated_user()
    return UserSerializer(only=('id', 'name', 'email', 'contact', 'address', 'is_admin', 'profile')).jsonify(user)
