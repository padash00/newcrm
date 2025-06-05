from . import db

class Promotion(db.Model):
    __tablename__ = 'promotions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    pattern = db.Column(db.String(50))
    schedule = db.Column(db.JSON)
