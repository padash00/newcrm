from . import db

class Zone(db.Model):
    __tablename__ = 'zones'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    computers = db.relationship('Computer', back_populates='zone')
    bookings = db.relationship('Booking', back_populates='zone')
