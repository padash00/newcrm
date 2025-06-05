from datetime import datetime
from . import db

class Payment(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    method = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    shift_id = db.Column(db.Integer, db.ForeignKey('shifts.id'))

    client = db.relationship('Client', back_populates='payments')
    shift = db.relationship('Shift', back_populates='payments')
