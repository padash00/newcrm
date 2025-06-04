from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    jwt_required, get_jwt_identity
)
from werkzeug.security import check_password_hash

from models import db
from models.users import User


auth_bp = Blueprint('auth', __name__, url_prefix='/api')


@auth_bp.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'msg': 'Missing credentials'}), 400

    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({'msg': 'Bad credentials'}), 401

    token = create_access_token(identity=user.id)
    return jsonify(access_token=token), 200


@auth_bp.route('/protected')
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200
