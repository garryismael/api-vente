from flask import jsonify
from flask_pydantic import validate
from sqlalchemy.orm import joinedload
from src.app import app
from src.models.purchase import Purchase
from src.serializers.purchase import purchase_schemas, purchase_schema
from src.utils.auth import admin_required


@app.get("/admin/purchases")
@admin_required()
def all_purchases_admin():
    purchases = Purchase.query.options(joinedload(Purchase.product)).all()
    return purchase_schemas.jsonify(purchases)

@app.get("/admin/purchases/<id>")
@validate()
@admin_required()
def get_one_purchase_admin(id:int):
    purchase = Purchase.query.filter_by(id=id).first_or_404()
    return purchase_schema.jsonify(purchase)

@app.delete("/admin/purchases/<int:id>")
@validate()
@admin_required()
def delete_purchase_admin(id: int):
    purchase: Purchase = Purchase.query.filter_by(id=id).first_or_404()
    purchase.delete()
    return jsonify(), 200
