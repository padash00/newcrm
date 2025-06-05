from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from .utils import role_required

from models import db
from models.promotions import Promotion

promos_bp = Blueprint('promotions', __name__, url_prefix='/api/promotions')

@promos_bp.route('/', methods=['GET'])
@jwt_required()
@role_required(['admin'])
def list_promotions():
    promos = Promotion.query.all()
    return jsonify([{ 'id': p.id, 'name': p.name, 'pattern': p.pattern, 'schedule': p.schedule } for p in promos])

@promos_bp.route('/', methods=['POST'])
@jwt_required()
@role_required(['admin'])
def create_promotion():
    data = request.get_json() or {}
    name = data.get('name')
    if not name:
        return jsonify({'msg': 'name required'}), 400
    promo = Promotion(name=name, pattern=data.get('pattern'), schedule=data.get('schedule'))
    db.session.add(promo)
    db.session.commit()
    return jsonify({'id': promo.id}), 201
