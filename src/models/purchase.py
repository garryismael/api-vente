from datetime import date

from sqlalchemy import Column, Date, ForeignKey, Integer
from src.config.database import db
from src.models.user import User
from src.schemas.purchase import PurchaseBase



class Purchase(db.Model):
    __tablename__ = 'purchases'
    id = Column(Integer, primary_key=True, autoincrement=True)
    quantity = Column(Integer)
    date_purchase = Column(Date, nullable=False, default=date.today())
    client_id = Column(Integer, ForeignKey('users.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    
    client = db.relationship('User', backref=db.backref('users', lazy='dynamic'))
    product = db.relationship('Product', backref=db.backref('products', lazy='dynamic'))
    
    def __init__(self, *,client_id: int, product_id: int, quantity: int) -> None:
        self.init(product_id, quantity)
        self.client_id = client_id
        
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def update(self, data: PurchaseBase):
        self.init(**data.dict())
        db.session.commit()
        return self
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def init(self, product_id, quantity):
        self.product_id = product_id
        self.quantity = quantity
        
    @staticmethod
    def bulk_create(user: User, body: list[PurchaseBase]):
        if len(body) > 0:
            purchases = [Purchase(client_id=user.id, **purchase.dict()) for purchase in body]
            db.session.bulk_save_objects(purchases)
            db.session.commit()
    
    @staticmethod
    def bulk_update(user: User, body: list[PurchaseBase]):
        if len(body) > 0:
            purchases = [Purchase(client_id=user.id, **purchase.dict()) for purchase in body]
            db.session.bulk_update_mappings(purchases)
            db.session.commit()
            
    def __repr__(self):
        return f'<Order {self.client}>'
