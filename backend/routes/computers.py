from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from .utils import role_required

from models import db
from models.computers import Computer
from models.zones import Zone

computers_bp = Blueprint('computers', __name__, url_prefix='/api/computers')

@computers_bp.route('/', methods=['GET'])
@jwt_required()
@role_required(['admin', 'tech'])
def list_computers():
    comps = Computer.query.all()
    return jsonify([{ 'id': c.id, 'name': c.name, 'zone_id': c.zone_id, 'status': c.status } for c in comps])

@computers_bp.route('/', methods=['POST'])
@jwt_required()
@role_required(['admin', 'tech'])
def create_computer():
    data = request.get_json() or {}
    name = data.get('name')
    zone_id = data.get('zone_id')
    status = data.get('status', 'free')
    if not all([name, zone_id]):
        return jsonify({'msg': 'name and zone_id required'}), 400
    if Computer.query.filter_by(name=name).first():
        return jsonify({'msg': 'computer exists'}), 409
    if not Zone.query.get(zone_id):
        return jsonify({'msg': 'zone not found'}), 404
    comp = Computer(name=name, zone_id=zone_id, status=status)
    db.session.add(comp)
    db.session.commit()
    return jsonify({'id': comp.id}), 201

@computers_bp.route('/<int:comp_id>', methods=['PATCH'])
@jwt_required()
@role_required(['admin', 'tech'])
def update_computer(comp_id):
    comp = Computer.query.get_or_404(comp_id)
    data = request.get_json() or {}
    if 'name' in data:
        if Computer.query.filter(Computer.name==data['name'], Computer.id!=comp_id).first():
            return jsonify({'msg': 'name exists'}), 409
        comp.name = data['name']
    if 'zone_id' in data:
        if not Zone.query.get(data['zone_id']):
            return jsonify({'msg': 'zone not found'}), 404
        comp.zone_id = data['zone_id']
    if 'status' in data:
        comp.status = data['status']
    db.session.commit()
    return jsonify({'msg': 'updated'})
