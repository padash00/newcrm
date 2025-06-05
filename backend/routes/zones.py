from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
bh21zy-codex/разработка-crm-системы-для-компьютерного-клуба
from .utils import role_required

codex/разработка-crm-системы-для-компьютерного-клуба
from .utils import role_required
main
main

from models import db
from models.zones import Zone

zones_bp = Blueprint('zones', __name__, url_prefix='/api/zones')

@zones_bp.route('/', methods=['GET'])
@jwt_required()
bh21zy-codex/разработка-crm-системы-для-компьютерного-клуба
@role_required(['admin'])

codex/разработка-crm-системы-для-компьютерного-клуба
@role_required(['admin'])
main
main
def list_zones():
    zones = Zone.query.all()
    return jsonify([{ 'id': z.id, 'name': z.name } for z in zones])

@zones_bp.route('/', methods=['POST'])
@jwt_required()
bh21zy-codex/разработка-crm-системы-для-компьютерного-клуба
@role_required(['admin'])

codex/разработка-crm-системы-для-компьютерного-клуба
@role_required(['admin'])
main
main
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
