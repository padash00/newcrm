from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity

from models.users import User


def role_required(roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            user = User.query.get(get_jwt_identity())
            if not user or user.role not in roles:
                return jsonify({'msg': 'forbidden'}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator
