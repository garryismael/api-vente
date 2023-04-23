from src.config.database import db
from sqlalchemy import text

SQL = "SELECT id, purchase_id, quantity, date_purchases, client_id, client_name, product_id, product_name, TO_CHAR(deleted_on, 'DD/MM/YYYY à HH:MM') as deleted_on FROM purchases_delete order by id"

def get_purchases_deleted():
    data = []
    results = db.session.execute(text(SQL))
    for result in results:
        data.append({
            'id': result.id,
            'purchase_id': result.purchase_id,
            'quantity': result.quantity,
            'date_purchases': result.date_purchases,
            'client_id': result.client_id,
            'client_name': result.client_name,
            'product_id': result.product_id,
            'product_name': result.product_name,
            'deleted_on': result.deleted_on
        })
    return data