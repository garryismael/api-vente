from flask_jwt_extended import jwt_required, verify_jwt_in_request
from pydantic import BaseModel, EmailStr, Field, validator
from src.models.user import User
from src.utils.auth import get_authenticated_user
from werkzeug.security import check_password_hash

class UserBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    profile: str = Field(..., min_length=3, max_length=255)
    address: str = Field(..., min_length=3, max_length=50)
    contact: str = Field(..., min_length=3, max_length=50)
    email: EmailStr

    class Config:
        orm_mode = True

class UserCreate(UserBase):
    password: str
    
    @validator('email')
    def email_must_be_unique(cls, v):
        user = User.query.filter_by(email=v).first()
        if user is not None:
            raise ValueError('email must be unique')
        return v
class UserDb(UserBase):
    id: int
    is_admin: bool

class UserDbList(BaseModel):
    users: list[UserDb]
    
    class Config:
        orm_mode = True
        

class UserLogin(BaseModel):
    email: EmailStr
    password: str

    @validator('email')
    def email_exists(cls, v):
        user = User.query.filter_by(email=v).first()
        if user is None:
            raise ValueError('invalid email or password')
        return v
    
    @validator("password")
    def password_match(cls, v, values, **kwargs):
        email = values['email']
        user = User.query.filter_by(email=email).first_or_404()
        if not check_password_hash(user.password, v):
            raise ValueError('invalid email or password')
        return v

class UserPassword(BaseModel):
    prevPassword: str = Field(..., min_length=3)
    newPassword: str = Field(..., min_length=3)
    
    @validator("prevPassword")
    def password_match(cls, v):
        verify_jwt_in_request()
        user: User = get_authenticated_user()
        if not check_password_hash(user.password, v):
            raise ValueError('Password don\'t match')
        return v
