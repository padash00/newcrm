from datetime import datetime
from . import db

class Client(db.Model):
    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    balance = db.Column(db.Float, default=0.0)
    debt = db.Column(db.Float, default=0.0)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    bookings = db.relationship('Booking', back_populates='client')
    sessions = db.relationship('Session', back_populates='client')
    payments = db.relationship('Payment', back_populates='client')
