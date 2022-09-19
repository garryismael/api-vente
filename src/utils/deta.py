from os import environ

from werkzeug.datastructures import FileStorage

from deta import Deta

DETA_PROJECT_KEY = environ.get('DETA_PROJECT_KEY')
deta = Deta(DETA_PROJECT_KEY)

product_drive = deta.Drive("products")


def upload_file(file: FileStorage, filename: str):
    product_drive.put(filename, file.stream.read())
    file.close()
    return filename

def delete_file(filename: str):
    product_drive.delete(filename)
    
def download_file(filename: str):
    return product_drive.get(filename)
