from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from flask_pydantic import validate
from src.config.database import db
from src.models.product import Product
from src.models.purchase import Purchase
from src.models.user import User
from src.schemas.purchase import PurchaseBaseList
from src.serializers.purchase import purchase_serializer, purchases_serializer
from src.utils.auth import get_authenticated_user
from src.utils.purchase import get_products_ids_not_found_in_db

purchase_bp = Blueprint('purchase_bp', __name__, url_prefix="/purchases")

@purchase_bp.get("/")
@jwt_required()
def all_purchases():
    user = get_authenticated_user()
    purchases = Purchase.query.filter_by(client_id=user.id)
    return purchases_serializer.jsonify(purchases)

@purchase_bp.get("/<id>")
@validate()
@jwt_required()
def get_one_purchase(id:int):
    user: User = get_authenticated_user()
    purchase = Purchase.query.filter_by(id=id, client_id=user.id).first_or_404()
    return purchase_serializer.jsonify(purchase)

@purchase_bp.post("/")
@validate()
@jwt_required()
def create_purchase(body: PurchaseBaseList):
    user: User = get_authenticated_user()
    products_ids = [purchase.product_id for purchase in body.items]
    products_ids_in_db: list[tuple[int]] = Product.query.with_entities(Product.id).filter(Product.id.in_(products_ids)).all()
    products_not_found = get_products_ids_not_found_in_db(products_ids, products_ids_in_db)
    if len(products_not_found) > 0:
        return jsonify(products_not_found=products_not_found), 412
    Purchase.bulk_create(user, body.items)
    return jsonify(""), 201

@purchase_bp.put("/<int:id>")
@validate()
@jwt_required()
def edit_purchase(id: int, body: PurchaseBaseList):
    user: User = get_authenticated_user()
    purchase = Purchase.query.filter_by(id=id, client_id=user.id).first_or_404()
    purchase.update(body)
    return purchase_serializer.jsonify(purchase)

@purchase_bp.delete("/<int:id>")
@validate()
@jwt_required()
def delete_purchase(id: int):
    user: User = get_authenticated_user()
    purchase: Purchase = Purchase.query.filter_by(id=id, client_id=user.id).first_or_404()
    purchase.delete()
    return jsonify(), 200
