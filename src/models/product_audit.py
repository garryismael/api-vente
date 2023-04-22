from src.config.database import db
from sqlalchemy import text

SQL = "SELECT id, product_id, name, price, description, image, TO_CHAR(changed_on, 'DD/MM/YYYY à HH:MM') as changed_on FROM product_audits order by id"

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