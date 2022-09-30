from functools import wraps
from pydantic import ValidationError
from flask import jsonify
from werkzeug.exceptions import NotFound

def valid_form(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except ValidationError as e:
            return jsonify(errors=e.errors()), 412
        except NotFound as e:
            return jsonify(msg='Model Not Found'), 404
        except Exception as e:
            print(e)
            return jsonify(msg="Not a valid form"), 400
    return wrapper