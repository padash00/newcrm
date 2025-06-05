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
codex/разработка-crm-системы-для-компьютерного-клуба
    return jsonify(access_token=token, role=user.role), 200



    return jsonify(access_token=token), 200


codex-ui-clean
main
@auth_bp.route('/auth/register', methods=['POST'])
def register():
    """Create a new user account."""
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')
    full_name = data.get('full_name')
    phone = data.get('phone')
    role_id = data.get('role_id')

    if not all([username, password, full_name, phone, role_id]):
        return jsonify({'msg': 'Missing required fields'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'msg': 'Username already exists'}), 409

    user = User(
        username=username,
        full_name=full_name,
        phone=phone,
        role_id=role_id,
    )
codex/разработка-crm-системы-для-компьютерного-клуба
    if user.role_rel:
        user.role = user.role_rel.name
 main
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({'msg': 'User created', 'id': user.id}), 201


 codex/разработка-crm-системы-для-компьютерного-клуба

 main
 main
@auth_bp.route('/protected')
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200
