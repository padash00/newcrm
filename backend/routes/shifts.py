codex/разработка-crm-системы-для-компьютерного-клуба
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify, send_file
import openpyxl
from io import BytesIO
from flask_jwt_extended import jwt_required, get_jwt_identity
from .utils import role_required

from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
main

from models import db
from models.shifts import Shift

shifts_bp = Blueprint('shifts', __name__, url_prefix='/api/shifts')

@shifts_bp.route('/', methods=['GET'])
@jwt_required()
codex/разработка-crm-системы-для-компьютерного-клуба
@role_required(['operator', 'admin'])
main
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
codex/разработка-crm-системы-для-компьютерного-клуба
@role_required(['operator', 'admin'])
main
def open_shift():
    operator_id = get_jwt_identity()
    shift = Shift(operator_id=operator_id, start_time=datetime.utcnow())
    db.session.add(shift)
    db.session.commit()
    return jsonify({'id': shift.id}), 201

@shifts_bp.route('/close', methods=['POST'])
@jwt_required()
codex/разработка-crm-системы-для-компьютерного-клуба
@role_required(['operator', 'admin'])
main
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
codex/разработка-crm-системы-для-компьютерного-клуба
@role_required(['operator', 'admin'])
main
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
codex/разработка-crm-системы-для-компьютерного-клуба


@shifts_bp.route('/export_excel', methods=['GET'])
@jwt_required()
@role_required(['operator', 'admin'])
def export_shifts_excel():
    """Export shifts to an Excel file for bookkeeping."""
    range_days = int(request.args.get('range', 30))
    end = datetime.utcnow()
    start = end - timedelta(days=range_days)
    shifts = Shift.query.filter(Shift.start_time >= start).all()

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(['Дата', 'Оператор', 'Касса', 'Kaspi', 'Долги', 'Мелочь', 'Разница', 'Комментарий'])
    for s in shifts:
        total_cash = s.cash_amount + s.kaspi_amount + s.coins_amount + s.debt_amount
        ws.append([
            s.start_time.date().isoformat(),
            s.operator.full_name if s.operator else s.operator_id,
            total_cash,
            s.kaspi_amount,
            s.debt_amount,
            s.coins_amount,
            s.delta_amount,
            s.comment or ''
        ])

    output = BytesIO()
    wb.save(output)
    output.seek(0)
    return send_file(
        output,
        as_attachment=True,
        download_name='shifts.xlsx',
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
main
