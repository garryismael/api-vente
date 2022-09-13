from sqlalchemy import Boolean, Column, Integer, String
from src.config.database import db


class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(length=50), nullable=False)
    address = Column(String(length=50),nullable=False)
    email = Column(String(length=255))
    is_admin = Column(Boolean())
    hashed_password = Column(String(length=255))
    
    
    def __repr__(self):
        return f'<User {self.name}>'
