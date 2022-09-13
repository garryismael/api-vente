from sqlalchemy import Column, Float, Integer, String
from src.config.database import db


class Product(db.Model):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)

    def __repr__(self):
        return f'<User {self.name}>'
