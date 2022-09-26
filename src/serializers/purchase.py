from src.app import ma
from src.models.purchase import Purchase
from marshmallow.fields import Nested
from src.serializers.product import ProductSerializer

from src.serializers.user import UserSerializer

class PurchaseSerializer(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Purchase
        include_fk = True
        load_instance = True
    

class PurchaseSchema(ma.SQLAlchemyAutoSchema):
    client = Nested(UserSerializer, only=("id", 'name', 'profile'))
    product = Nested(ProductSerializer, only=('id','name', 'image'))
    class Meta:
        model = Purchase
        include_fk = True
        load_instance = True
        
purchase_serializer = PurchaseSerializer()
purchases_serializer = PurchaseSerializer(many=True)
purchase_schema = PurchaseSchema(exclude=('product_id', 'client_id'))
purchase_schemas = PurchaseSchema(many=True, exclude=('product_id', 'client_id'))