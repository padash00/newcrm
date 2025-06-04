from datetime import datetime
from . import db

class Shift(db.Model):
    __tablename__ = 'shifts'

    id = db.Column(db.Integer, primary_key=True)
    operator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime)
    kaspi_amount = db.Column(db.Float, default=0.0)
    cash_amount = db.Column(db.Float, default=0.0)
    coins_amount = db.Column(db.Float, default=0.0)
    debt_amount = db.Column(db.Float, default=0.0)

    operator = db.relationship('User', back_populates='shifts')
    payments = db.relationship('Payment', back_populates='shift')
