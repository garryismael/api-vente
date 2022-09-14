from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from flask_pydantic import validate
from src.models.purchase import Purchase
from src.models.user import User
from src.schemas.purchase import PurchaseBase
from src.serializers.purchase import purchase_serializer, purchases_serializer
from src.utils.auth import get_authenticated_user

purchase_bp = Blueprint('purchase_bp', __name__, url_prefix="/purchases")

@purchase_bp.get("/")
@jwt_required()
def all_purchases():
    user = get_authenticated_user()
    purchases = Purchase.query.filter(client_id=user.id)
    return purchases_serializer.jsonify(purchases)

@purchase_bp.get("/<id>")
@validate()
@jwt_required()
def get_one_purchase(id:int):
    user: User = get_authenticated_user()
    purchase = Purchase.query.filter_by(id=id, client_id=user.id).first_or_404()
    return purchase_serializer.jsonify(purchase)

@purchase_bp.post("/")
@validate
@jwt_required()
def create_purchase(body: list[PurchaseBase]):
    user: User = get_authenticated_user()
    ids = [purchase.product_id for purchase in body]
    Purchase.bulk_create(user, body)
    purchases = Purchase.query.filter_by(product_id__in=ids)
    return purchase_serializer.jsonify(purchases)
    
@purchase_bp.put("/<int:id>")
@validate()
@jwt_required()
def edit_purchase(id: int, body: PurchaseBase):
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
