from flask import jsonify
from flask_pydantic import validate
from src.app import app
from src.models.purchase import Purchase
from src.serializers.purchase import purchase_serializer, purchases_serializer
from src.utils.auth import admin_required


@app.get("/admin/purchases")
@admin_required()
def all_purchases():
    purchases = Purchase.query.all()
    return purchases_serializer.jsonify(purchases)

@app.get("/admin/purchases/<id>")
@validate()
@admin_required()
def get_one_purchase(id:int):
    purchase = Purchase.query.filter_by(id=id).first_or_404()
    return purchase_serializer.jsonify(purchase)

@app.delete("/admin/purchases/<int:id>")
@validate()
@admin_required()
def delete_purchase(id: int):
    purchase: Purchase = Purchase.query.filter_by(id=id).first_or_404()
    purchase.delete()
    return jsonify(), 200
