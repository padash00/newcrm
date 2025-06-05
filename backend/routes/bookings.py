from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from models import db
from models.bookings import Booking

bookings_bp = Blueprint('bookings', __name__, url_prefix='/api/bookings')

@bookings_bp.route('/', methods=['POST'])
@jwt_required()
def create_booking():
    data = request.get_json() or {}
    try:
        start = datetime.fromisoformat(data.get('start_time'))
    except Exception:
        return jsonify({'msg': 'bad start_time'}), 400
    booking = Booking(
        client_id=data.get('client_id'),
        zone_id=data.get('zone_id'),
        num_pcs=data.get('num_pcs'),
        start_time=start,
        duration=data.get('duration'),
        status='active'
    )
    db.session.add(booking)
    db.session.commit()
    return jsonify({'id': booking.id}), 201

@bookings_bp.route('/', methods=['GET'])
@jwt_required()
def list_bookings():
    date = request.args.get('date')
    status = request.args.get('status')
    query = Booking.query
    if date:
        try:
            dt = datetime.fromisoformat(date)
            end = dt.replace(hour=23, minute=59, second=59)
            query = query.filter(Booking.start_time >= dt, Booking.start_time <= end)
        except ValueError:
            pass
    if status:
        query = query.filter_by(status=status)
    bookings = query.all()
    return jsonify([
        {
            'id': b.id,
            'client_id': b.client_id,
            'zone_id': b.zone_id,
            'num_pcs': b.num_pcs,
            'start_time': b.start_time.isoformat(),
            'duration': b.duration,
            'status': b.status,
        } for b in bookings
    ])

@bookings_bp.route('/<int:booking_id>/cancel', methods=['POST'])
@jwt_required()
def cancel_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    booking.status = 'cancelled'
    db.session.commit()
    return jsonify({'msg': 'cancelled'})
