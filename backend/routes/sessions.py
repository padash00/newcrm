from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from models import db
from models.sessions import Session
from models.computers import Computer
from models.tariffs import Tariff
from models.clients import Client

sessions_bp = Blueprint('sessions', __name__, url_prefix='/api/sessions')

@sessions_bp.route('/start', methods=['POST'])
@jwt_required()
def start_session():
    data = request.get_json() or {}
    client_id = data.get('client_id')
    computer_id = data.get('computer_id')
    tariff_id = data.get('tariff_id')
    if not all([client_id, computer_id, tariff_id]):
        return jsonify({'msg': 'Missing data'}), 400
    computer = Computer.query.get_or_404(computer_id)
    if computer.status != 'free':
        return jsonify({'msg': 'Computer not available'}), 400
    computer.status = 'busy'
    session = Session(
        client_id=client_id,
        computer_id=computer_id,
        tariff_id=tariff_id,
        start_time=datetime.utcnow()
    )
    db.session.add(session)
    db.session.commit()
    return jsonify({'id': session.id}), 201

@sessions_bp.route('/stop', methods=['POST'])
@jwt_required()
def stop_session():
    data = request.get_json() or {}
    session_id = data.get('id')
    session = Session.query.get_or_404(session_id)
    if session.end_time:
        return jsonify({'msg': 'Session already stopped'}), 400
    session.end_time = datetime.utcnow()
    duration_hours = (session.end_time - session.start_time).total_seconds() / 3600
    tariff = Tariff.query.get(session.tariff_id)
    session.cost = round(duration_hours * tariff.price_per_hour, 2) if tariff else 0
    comp = Computer.query.get(session.computer_id)
    if comp:
        comp.status = 'free'
    db.session.commit()
    return jsonify({'cost': session.cost})

@sessions_bp.route('/', methods=['GET'])
@jwt_required()
def list_sessions():
    client_id = request.args.get('client_id')
    date = request.args.get('date')  # YYYY-MM-DD
    query = Session.query
    if client_id:
        query = query.filter_by(client_id=client_id)
    if date:
        try:
            dt = datetime.fromisoformat(date)
            next_day = dt.replace(hour=23, minute=59, second=59)
            query = query.filter(Session.start_time >= dt, Session.start_time <= next_day)
        except ValueError:
            pass
    sessions = query.all()
    return jsonify([{ 
        'id': s.id,
        'client_id': s.client_id,
        'computer_id': s.computer_id,
        'tariff_id': s.tariff_id,
        'start_time': s.start_time.isoformat(),
        'end_time': s.end_time.isoformat() if s.end_time else None,
        'cost': s.cost,
    } for s in sessions])
