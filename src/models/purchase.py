from datetime import date

from sqlalchemy import Column, Date, ForeignKey, Integer
from src.config.database import db


class Purchase(db.Model):
    __tablename__ = 'purchases'
    id = Column(Integer, primary_key=True, autoincrement=True)
    quantity = Column(Integer)
    date_order = Column(Date, nullable=False, default=date.today())
    client_id = Column(Integer, ForeignKey('users.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    
    client = db.relationship('User', backref=db.backref('purchases', lazy=True))
    product = db.relationship('Product', backref=db.backref('products', lazy=True))
    
    def __repr__(self):
        return f'<Order {self.client}>'
