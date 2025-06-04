from . import db

class Tariff(db.Model):
    __tablename__ = 'tariffs'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price_per_hour = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)

    sessions = db.relationship('Session', back_populates='tariff')
