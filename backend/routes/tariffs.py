from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
bh21zy-codex/разработка-crm-системы-для-компьютерного-клуба
from .utils import role_required

codex/разработка-crm-системы-для-компьютерного-клуба
from .utils import role_required
main
main

from models import db
from models.tariffs import Tariff


tariffs_bp = Blueprint('tariffs', __name__, url_prefix='/api/tariffs')

@tariffs_bp.route('/', methods=['GET'])
@jwt_required()
bh21zy-codex/разработка-crm-системы-для-компьютерного-клуба
@role_required(['admin'])

codex/разработка-crm-системы-для-компьютерного-клуба
@role_required(['admin'])
main
main
def list_tariffs():
    tariffs = Tariff.query.all()
    return jsonify([{ 'id': t.id, 'name': t.name, 'price_per_hour': t.price_per_hour, 'description': t.description } for t in tariffs])

@tariffs_bp.route('/', methods=['POST'])
@jwt_required()
bh21zy-codex/разработка-crm-системы-для-компьютерного-клуба
@role_required(['admin'])

codex/разработка-crm-системы-для-компьютерного-клуба
@role_required(['admin'])
main
main
def create_tariff():
    data = request.get_json() or {}
    if not all([data.get('name'), data.get('price_per_hour')]):
        return jsonify({'msg': 'name and price_per_hour required'}), 400
    tariff = Tariff(
        name=data['name'],
        price_per_hour=data['price_per_hour'],
        description=data.get('description')
    )
    db.session.add(tariff)
    db.session.commit()
    return jsonify({'id': tariff.id}), 201
