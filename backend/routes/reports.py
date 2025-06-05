from datetime import datetime, timedelta, date, time
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from models.sessions import Session
from models.payments import Payment
from models.shifts import Shift
from .utils import role_required

reports_bp = Blueprint('reports', __name__, url_prefix='/api/reports')


def _day_range(d: date):
    start = datetime.combine(d, time.min)
    end = datetime.combine(d, time.max)
    return start, end


def _day_totals(d: date):
    start, end = _day_range(d)
    payments = Payment.query.filter(Payment.created_at >= start, Payment.created_at <= end).all()
    sessions = Session.query.filter(Session.start_time >= start, Session.start_time <= end).all()
    return {
        'date': d.isoformat(),
        'total_cash': sum(p.amount for p in payments if p.method == 'cash'),
        'total_kaspi': sum(p.amount for p in payments if p.method == 'kaspi'),
        'total_debt': sum(p.amount for p in payments if p.method == 'debt'),
        'total_sessions': len(sessions),
        'total_clients': len({s.client_id for s in sessions})
    }


@reports_bp.route('/daily')
@jwt_required()
@role_required(['operator', 'admin'])
def daily_report():
    today = date.today()
    return jsonify(_day_totals(today))


@reports_bp.route('/weekly')
@jwt_required()
@role_required(['operator', 'admin'])
def weekly_report():
    today = date.today()
    start = today - timedelta(days=today.weekday())
    data = [_day_totals(start + timedelta(days=i)) for i in range(7)]
    return jsonify(data)


@reports_bp.route('/custom')
@jwt_required()
@role_required(['operator', 'admin'])
def custom_report():
    from_str = request.args.get('from')
    to_str = request.args.get('to')
    if not from_str or not to_str:
        return jsonify({'msg': 'from and to required'}), 400
    try:
        start_date = datetime.fromisoformat(from_str).date()
        end_date = datetime.fromisoformat(to_str).date()
    except ValueError:
        return jsonify({'msg': 'bad date'}), 400
    if start_date > end_date:
        start_date, end_date = end_date, start_date
    data = []
    d = start_date
    while d <= end_date:
        data.append(_day_totals(d))
        d += timedelta(days=1)
    return jsonify(data)


@reports_bp.route('/income-by-day')
@jwt_required()
@role_required(['operator', 'admin'])
def income_by_day():
    rng = int(request.args.get('range', 7))
    today = date.today()
    data = []
    for i in range(rng):
        d = today - timedelta(days=i)
        totals = _day_totals(d)
        totals['income'] = totals['total_cash'] + totals['total_kaspi']
        data.append({'date': totals['date'], 'income': totals['income']})
    return jsonify(list(reversed(data)))


@reports_bp.route('/clients-active')
@jwt_required()
@role_required(['operator', 'admin'])
def clients_active():
    rng = int(request.args.get('range', 30))
    today = date.today()
    data = []
    for i in range(rng):
        d = today - timedelta(days=i)
        totals = _day_totals(d)
        data.append({'date': totals['date'], 'clients': totals['total_clients']})
    return jsonify(list(reversed(data)))


@reports_bp.route('/shift-performance')
@jwt_required()
@role_required(['operator', 'admin'])
def shift_performance():
    shifts = Shift.query.all()
    count = len(shifts)
    total = sum(s.total_amount for s in shifts)
    avg = round(total / count, 2) if count else 0
    return jsonify({'shifts': count, 'average_income': avg})
