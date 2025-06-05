from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from models import db
from models.shifts import Shift

shifts_bp = Blueprint('shifts', __name__, url_prefix='/api/shifts')

@shifts_bp.route('/', methods=['GET'])
@jwt_required()
def list_shifts():
    shifts = Shift.query.all()
    return jsonify([{ 
        'id': s.id,
        'operator_id': s.operator_id,
        'start_time': s.start_time.isoformat() if s.start_time else None,
        'end_time': s.end_time.isoformat() if s.end_time else None,
        'kaspi_amount': s.kaspi_amount,
        'cash_amount': s.cash_amount,
        'coins_amount': s.coins_amount,
        'debt_amount': s.debt_amount,
        'comment': s.comment,
        'total_amount': s.total_amount,
        'delta_amount': s.delta_amount,
    } for s in shifts])

@shifts_bp.route('/', methods=['POST'])
@jwt_required()
def open_shift():
    operator_id = get_jwt_identity()
    shift = Shift(operator_id=operator_id, start_time=datetime.utcnow())
    db.session.add(shift)
    db.session.commit()
    return jsonify({'id': shift.id}), 201

@shifts_bp.route('/close', methods=['POST'])
@jwt_required()
def close_shift():
    operator_id = get_jwt_identity()
    data = request.get_json() or {}
    shift = Shift.query.filter_by(operator_id=operator_id, end_time=None).first()
    if not shift:
        return jsonify({'msg': 'No open shift'}), 400
    shift.end_time = datetime.utcnow()
    shift.kaspi_amount = data.get('kaspi_amount', 0.0)
    shift.cash_amount = data.get('cash_amount', 0.0)
    shift.coins_amount = data.get('coins_amount', 0.0)
    shift.debt_amount = data.get('debt_amount', 0.0)
    shift.comment = data.get('comment')
    declared_total = (
        shift.kaspi_amount + shift.cash_amount + shift.coins_amount + shift.debt_amount
    )
    shift.total_amount = declared_total
    actual_total = sum(p.amount for p in shift.payments)
    shift.delta_amount = round(declared_total - actual_total, 2)
    db.session.commit()
    return jsonify({'msg': 'shift closed', 'id': shift.id, 'delta': shift.delta_amount})

@shifts_bp.route('/<int:shift_id>', methods=['GET'])
@jwt_required()
def get_shift(shift_id):
    shift = Shift.query.get_or_404(shift_id)
    return jsonify({
        'id': shift.id,
        'operator_id': shift.operator_id,
        'start_time': shift.start_time.isoformat() if shift.start_time else None,
        'end_time': shift.end_time.isoformat() if shift.end_time else None,
        'kaspi_amount': shift.kaspi_amount,
        'cash_amount': shift.cash_amount,
        'coins_amount': shift.coins_amount,
        'debt_amount': shift.debt_amount,
        'comment': shift.comment,
        'total_amount': shift.total_amount,
        'delta_amount': shift.delta_amount,
    })
