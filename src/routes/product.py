
from flask import jsonify, request, send_from_directory
from flask_pydantic import validate
from src.app import app
from src.models.product import Product
from src.schemas.product import ProductBase, ProductDb
from src.serializers.product import product_serializer, products_serializer
from src.utils.auth import admin_required
from src.utils.form import valid_form
from src.utils.media import upload_file
from werkzeug.utils import secure_filename
from src.models.product_audit import get_products_audits

product_folder = app.config.get('UPLOAD_PRODUCTS_FOLDER')

@app.get('/products')
def all_products():
    search = request.args.get('search', None)
    products = Product.query.order_by(Product.name).all() if (search is None or search == '') else Product.query.order_by(Product.name).filter(Product.name.ilike(f'{search}%'))
    return products_serializer.jsonify(products)

@app.get('/products/audits')
def all_product_audits():
    return get_products_audits()


@app.get("/products/<int:id>")
@validate()
def get_one_product(id:int):
    product = Product.query.filter_by(id=id).first_or_404()
    return ProductDb.from_orm(product)

@app.get("/products/images/<name>")
def get_product_image(name: str):
    return send_from_directory(product_folder, name)

@app.post("/products")
@valid_form
@admin_required()
def create_product():
    data = dict(request.form)
    image = request.files.get('image')
    filename = secure_filename(image.filename)
    body = ProductBase(**data, image=filename)
    product: Product = product_serializer.load(data=body.dict())
    product = product.create()
    upload_file(image, product_folder, filename)
    return product_serializer.jsonify(product)

@app.put("/products/<int:id>")
@valid_form
@admin_required()
def edit_product(id: int):
    product: Product = Product.query.filter_by(id=id).first_or_404()
    data = dict(request.form)
    
    if 'image' in data:
        del data['image']
        
    image = request.files.get('image')
    filename = product.image
    if image is not None and image.filename != '':
        filename = secure_filename(image.filename)
    body = ProductBase(**data, image=filename)
    product = product.update(body.dict())
    if image is not None and image.filename != '':
        upload_file(image, product_folder, filename)
    return product_serializer.jsonify(product)
    

@app.delete("/products/<int:id>")
@validate()
@admin_required()
def delete_product(id: int):
    product: Product = Product.query.filter_by(id=id).first_or_404()
    product.delete()
    return jsonify(""), 200
