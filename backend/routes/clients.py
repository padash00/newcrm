from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from models import db
from models.clients import Client

clients_bp = Blueprint('clients', __name__, url_prefix='/api/clients')

@clients_bp.route('/', methods=['GET'])
@jwt_required()
def get_clients():
    clients = Client.query.all()
    return jsonify([{
        'id': c.id,
        'full_name': c.full_name,
        'phone': c.phone,
        'balance': c.balance,
        'debt': c.debt,
        'notes': c.notes,
    } for c in clients])

@clients_bp.route('/', methods=['POST'])
@jwt_required()
def create_client():
    data = request.get_json() or {}
    client = Client(
        full_name=data.get('full_name'),
        phone=data.get('phone'),
        balance=data.get('balance', 0.0),
        debt=data.get('debt', 0.0),
        notes=data.get('notes'),
    )
    db.session.add(client)
    db.session.commit()
    return jsonify({'id': client.id}), 201

@clients_bp.route('/<int:client_id>', methods=['GET'])
@jwt_required()
def get_client(client_id):
    client = Client.query.get_or_404(client_id)
    return jsonify({
        'id': client.id,
        'full_name': client.full_name,
        'phone': client.phone,
        'balance': client.balance,
        'debt': client.debt,
        'notes': client.notes,
    })

@clients_bp.route('/<int:client_id>', methods=['PUT'])
@jwt_required()
def update_client(client_id):
    client = Client.query.get_or_404(client_id)
    data = request.get_json() or {}
    client.full_name = data.get('full_name', client.full_name)
    client.phone = data.get('phone', client.phone)
    client.balance = data.get('balance', client.balance)
    client.debt = data.get('debt', client.debt)
    client.notes = data.get('notes', client.notes)
    db.session.commit()
    return jsonify({'msg': 'updated'})

@clients_bp.route('/<int:client_id>', methods=['DELETE'])
@jwt_required()
def delete_client(client_id):
    client = Client.query.get_or_404(client_id)
    db.session.delete(client)
    db.session.commit()
    return jsonify({'msg': 'deleted'})
