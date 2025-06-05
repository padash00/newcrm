from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from .utils import role_required

from models import db
from models.zones import Zone

zones_bp = Blueprint('zones', __name__, url_prefix='/api/zones')

@zones_bp.route('/', methods=['GET'])
@jwt_required()
@role_required(['admin'])
def list_zones():
    zones = Zone.query.all()
    return jsonify([{ 'id': z.id, 'name': z.name } for z in zones])

@zones_bp.route('/', methods=['POST'])
@jwt_required()
@role_required(['admin'])
def create_zone():
    data = request.get_json() or {}
    name = data.get('name')
    if not name:
        return jsonify({'msg': 'name required'}), 400
    if Zone.query.filter_by(name=name).first():
        return jsonify({'msg': 'zone exists'}), 409
    zone = Zone(name=name)
    db.session.add(zone)
    db.session.commit()
    return jsonify({'id': zone.id}), 201
