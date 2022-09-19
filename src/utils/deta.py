import os

from werkzeug.datastructures import FileStorage

from deta import Deta
from src.app import app

DETA_PROJECT_KEY = os.environ.get('DETA_PROJECT_KEY')
deta = Deta(DETA_PROJECT_KEY)

product_drive = deta.Drive("products")


def upload_file(file: FileStorage, filename: str):
    file.save(os.path.join(app.config.get('UPLOAD_FOLDER'), filename))
    return filename

def delete_file(filename: str):
    product_drive.delete(filename)
    
def download_file(filename: str):
    return product_drive.get(filename)
