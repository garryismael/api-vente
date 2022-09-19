
from flask import Blueprint, jsonify, request, send_file
from flask_pydantic import validate
from src.models.product import Product
from src.schemas.product import ProductBase, ProductDb
from src.serializers.product import product_serializer, products_serializer
from src.utils.auth import admin_required
from src.utils.deta import delete_file, download_file, upload_file
from werkzeug.utils import secure_filename

from src.utils.form import valid_product_form

product_bp = Blueprint('product_bp', __name__, url_prefix="/products")

@product_bp.get("/")
def all_products():
    products = Product.query.all()
    return products_serializer.jsonify(products)

@product_bp.get("/<int:id>")
@validate()
def get_one_product(id:int):
    product = Product.query.filter_by(id=id).first_or_404()
    return ProductDb.from_orm(product)

@product_bp.get("image/<name>")
def get_image(name: str):
    file = download_file(name)
    if file is None:
        return jsonify(msg="Image Not Found"), 404
    return send_file(file, mimetype="image/png")

@product_bp.post("/")
@valid_product_form
@admin_required()
def create_product():
    data = dict(request.form)
    image = request.files.get('image')
    filename = secure_filename(image.filename)
    body = ProductBase(**data, image=filename)
    product: Product = product_serializer.load(data=body.dict())
    product = product.create()
    upload_file(image, filename)
    return product_serializer.jsonify(product)

@product_bp.put("/<int:id>")
@valid_product_form
@admin_required()
def edit_product(id: int):
    product: Product = Product.query.filter_by(id=id).first_or_404()
    data = dict(request.form)
    image = request.files.get('image')
    filename = product.image
    delete_filename: str = None
    if image is not None:
        delete_filename = filename
        filename = secure_filename(image.filename)
    body = ProductBase(**data, image=filename)
    product = product.update(body.dict())
    if image is not None:
        upload_file(image, filename)
        delete_file(delete_filename)
    return product_serializer.jsonify(product)
    

@product_bp.delete("/<int:id>")
@validate()
@admin_required()
def delete_product(id: int):
    product: Product = Product.query.filter_by(id=id).first_or_404()
    delete_file(product.image)
    product.delete()
    return jsonify(""), 200
