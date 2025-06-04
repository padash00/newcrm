from datetime import datetime
from . import db

class Session(db.Model):
    __tablename__ = 'sessions'

    id = db.Column(db.Integer, primary_key=True)
    computer_id = db.Column(db.Integer, db.ForeignKey('computers.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    tariff_id = db.Column(db.Integer, db.ForeignKey('tariffs.id'), nullable=False)
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime)
    cost = db.Column(db.Float, default=0.0)

    computer = db.relationship('Computer', back_populates='sessions')
    client = db.relationship('Client', back_populates='sessions')
    tariff = db.relationship('Tariff', back_populates='sessions')
