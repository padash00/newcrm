from . import db

class Computer(db.Model):
    __tablename__ = 'computers'

    id = db.Column(db.Integer, primary_key=True)
    zone_id = db.Column(db.Integer, db.ForeignKey('zones.id'), nullable=False)
    name = db.Column(db.String(50), unique=True, nullable=False)
    status = db.Column(db.String(20), default='free')

    zone = db.relationship('Zone', back_populates='computers')
    sessions = db.relationship('Session', back_populates='computer')
