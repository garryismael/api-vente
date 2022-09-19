from typing import Any
from sqlalchemy import Column, Float, Integer, String
from src.config.database import db

class Product(db.Model):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    price = Column(Float, nullable=False)
    description = Column(String(length=255), nullable=False)
    image = Column(String(255), nullable=False)

    def __init__(self, name, price, description,image):
        self.init(name,price, description, image)

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def update(self, data: dict[str, Any]):
        self.init(**data)
        db.session.commit()
        return self
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def init(self, name, price, description, image):
        self.name = name
        self.price = price
        self.image = image
        self.description = description

    
    def __repr__(self):
        return f'<User {self.name}>'
