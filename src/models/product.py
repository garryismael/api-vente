from typing import Any
from sqlalchemy import Column, Float, Integer, String
from src.config.database import db
from src.schemas.product import ProductBase


class Product(db.Model):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    price = Column(Float, nullable=False)
    image = Column(String(255), nullable=False)

    def __init__(self, name, price, image):
        self.init(name,price, image)

    def create(self):
        print(self.name, self.price, self.image)
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
    
    def init(self, name, price, image):
        self.name = name
        self.price = price
        self.image = image

    
    def __repr__(self):
        return f'<User {self.name}>'
