from src.config.database import db
from sqlalchemy import text

SQL = "SELECT id, product_id, name, price, description, image, TO_CHAR(changed_on, 'DD/MM/YYYY à HH:MM') as changed_on FROM product_audits order by id"

SQL_SELECT_DELETE = "SELECT id, product_id, name, price, description, TO_CHAR(deleted_on, 'DD/MM/YYYY à HH:MM') as deleted_on FROM product_delete order by id"

def get_products_audits():
    data = []
    results = db.session.execute(text(SQL))
    for result in results:
        data.append({
            'id': result.id,
            'product_id': result.product_id,
            'name': result.name,
            'price': result.price,
            'description': result.description,
            'image': result.image,
            'changed_on': result.changed_on
        })
    return data

def get_products_deleted():
    data = []
    results = db.session.execute(text(SQL_SELECT_DELETE))
    for result in results:
        data.append({
            'id': result.id,
            'product_id': result.product_id,
            'name': result.name,
            'price': result.price,
            'description': result.description,
            'deleted_on': result.deleted_on
        })
    return data