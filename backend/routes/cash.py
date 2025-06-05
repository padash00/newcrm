from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from models import db
from models.payments import Payment
from models.clients import Client

cash_bp = Blueprint('cash', __name__, url_prefix='/api/cash')

@cash_bp.route('/summary')
@jwt_required()
def cash_summary():
    date_str = request.args.get('date')
    if not date_str:
        return jsonify({'msg': 'date required'}), 400
    try:
        dt = datetime.fromisoformat(date_str)
    except ValueError:
        return jsonify({'msg': 'bad date'}), 400
    next_day = dt.replace(hour=23, minute=59, second=59)
    payments = Payment.query.filter(Payment.created_at >= dt, Payment.created_at <= next_day).all()
    summary = {'kaspi': 0.0, 'cash': 0.0, 'coins': 0.0, 'debt': 0.0}
    for p in payments:
        if p.method == 'kaspi':
            summary['kaspi'] += p.amount
        elif p.method == 'cash':
            summary['cash'] += p.amount
        elif p.method == 'coins':
            summary['coins'] += p.amount
        elif p.method == 'debt':
            summary['debt'] += p.amount
    return jsonify(summary)

@cash_bp.route('/history')
@jwt_required()
def cash_history():
    start = request.args.get('start')
    end = request.args.get('end')
    query = Payment.query
    if start:
        try:
            start_dt = datetime.fromisoformat(start)
            query = query.filter(Payment.created_at >= start_dt)
        except ValueError:
            pass
    if end:
        try:
            end_dt = datetime.fromisoformat(end)
            query = query.filter(Payment.created_at <= end_dt)
        except ValueError:
            pass
    payments = query.all()
    return jsonify([{ 'id': p.id, 'client_id': p.client_id, 'amount': p.amount, 'method': p.method, 'created_at': p.created_at.isoformat() } for p in payments])

@cash_bp.route('/client-debts')
@jwt_required()
def client_debts():
    clients = Client.query.filter(Client.debt > 0).all()
    return jsonify([{ 'id': c.id, 'full_name': c.full_name, 'debt': c.debt } for c in clients])
