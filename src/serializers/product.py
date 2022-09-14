from src.app import ma
from src.models.product import Product


class ProductSerializer(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        include_fk = True
        load_instance = True
    

product_serializer = ProductSerializer()
products_serializer = ProductSerializer(many=True)
