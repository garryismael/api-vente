from sqlalchemy import Boolean, Column, Integer, String
from src.config.database import db
from werkzeug.security import generate_password_hash


class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(length=50), nullable=False)
    profile = Column(String(length=255), nullable=False)
    address = Column(String(length=50),nullable=False)
    email = Column(String(length=255), unique=True, nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)
    password = Column(String(length=255), nullable=False)
    
    
    def __init__(self, *, name, profile, address, email, password):
        self.init(name, profile,address, email)
        self.password = generate_password_hash(password)
        

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def update(self, data):
        self.init(data.name, data.address, data.email)
        db.session.commit()
        return self
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    def init(self, name, profile, address, email):
        self.name = name
        self.profile = profile
        self.address = address
        self.email = email
        
    def __repr__(self):
        return f'<User {self.name}>'
