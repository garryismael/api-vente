from flask import Blueprint, jsonify
from flask_pydantic import validate
from src.models.product import Product
from src.schemas.product import ProductBase, ProductDb
from src.serializers.product import product_serializer, products_serializer
from src.utils.auth import admin_required

product_bp = Blueprint('product_bp', __name__, url_prefix="/products")

@product_bp.get("/")
def all_products():
    products = Product.query.all()
    return products_serializer.jsonify(products)

@product_bp.get("/<id>")
@validate()
def get_one_product(id:int):
    product = Product.query.filter_by(id=id).first_or_404()
    return ProductDb.from_orm(product)

@product_bp.post("/")
@validate()
@admin_required()
def create_product(body: ProductBase):
    product: Product = product_serializer.load(data=body.dict())
    product = product.create()
    return ProductDb.from_orm(product)

@product_bp.put("/<int:id>")
@validate()
@admin_required()
def edit_product(id: int, body: ProductBase):
    product: Product = Product.query.filter_by(id=id).first_or_404()
    product.update(body)
    return ProductDb.from_orm(product)


@product_bp.delete("/<int:id>")
@validate()
@admin_required()
def delete_product(id: int):
    product = Product.query.filter_by(id=id).first_or_404()
    product.delete()
    return jsonify(""), 200
