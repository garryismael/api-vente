from src.app import ma
from src.models.purchase import Purchase


class PurchaseSerializer(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Purchase
        include_fk = True
        load_instance = True
    

purchase_serializer = PurchaseSerializer()
purchases_serializer = PurchaseSerializer(many=True)
