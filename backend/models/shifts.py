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
bh21zy-codex/разработка-crm-системы-для-компьютерного-клуба

codex/разработка-crm-системы-для-компьютерного-клуба
main
    comment = db.Column(db.Text)
    total_amount = db.Column(db.Float, default=0.0)
    delta_amount = db.Column(db.Float, default=0.0)

bh21zy-codex/разработка-crm-системы-для-компьютерного-клуба

    codex-ui-clean
    comment = db.Column(db.Text)
    total_amount = db.Column(db.Float, default=0.0)
    delta_amount = db.Column(db.Float, default=0.0)
    main
main

main
    operator = db.relationship('User', back_populates='shifts')
    payments = db.relationship('Payment', back_populates='shift')
