from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
import openpyxl
from io import BytesIO

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


@clients_bp.route('/import_excel', methods=['POST'])
@jwt_required()
def import_clients_excel():
    """Import clients from an uploaded Excel (xlsx) file."""
    file = request.files.get('file')
    if not file:
        return jsonify({'msg': 'no file'}), 400

    try:
        workbook = openpyxl.load_workbook(file)
    except Exception:
        return jsonify({'msg': 'bad file'}), 400

    sheet = workbook.active
    added = 0
    errors = []
    for idx, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), start=2):
        full_name, phone, comment = row[:3]
        if not full_name:
            errors.append(f'row {idx}: empty name')
            continue
        if phone and Client.query.filter_by(phone=phone).first():
            # skip duplicates by phone number
            continue
        client = Client(full_name=full_name, phone=phone, notes=comment)
        db.session.add(client)
        added += 1
    db.session.commit()
    return jsonify({'added': added, 'errors': errors})
