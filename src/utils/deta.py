import os

from werkzeug.datastructures import FileStorage


def upload_file(file: FileStorage, path: str,filename: str):
    file.save(os.path.join(path, filename))
    return filename

