from sqlalchemy import Column, Float, Integer, String
from src.config.database import db
from src.schemas.product import ProductBase


class Product(db.Model):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)


    def __init__(self, name, price, stock):
        self.init(name,price, stock)

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def update(self, data: ProductBase):
        self.init(**data.dict())
        db.session.commit()
        return self
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def init(self, name, price, stock):
        self.name = name
        self.price = price
        self.stock = stock 

    
    def __repr__(self):
        return f'<User {self.name}>'
