# models/payment.py
from datetime import datetime
from enum import Enum

from sqlalchemy import CheckConstraint, Index
from sqlalchemy.orm import validates

from . import db


class PaymentMethod(str, Enum):
    CASH      = "cash"
    KASPI     = "kaspi"        # Kaspi QR / Kaspi Pay
    CARD      = "card"         # POS-терминал
    BALANCE   = "balance"      # списание с внутреннего счёта
    WRITE_OFF = "write_off"    # взаимозачёт / корректировка


class Payment(db.Model):
    __tablename__ = "payments"
    __table_args__ = (
        Index("ix_payments_client_date", "client_id", "created_at"),
        CheckConstraint("amount > 0", name="ck_payment_amount_positive"),
    )

    id         = db.Column(db.Integer, primary_key=True)
    client_id  = db.Column(
        db.Integer,
        db.ForeignKey("clients.id", ondelete="SET NULL"),
        nullable=True,      # позволяем платежам «без клиента» (разовое пополнение)
    )
    shift_id   = db.Column(
        db.Integer,
        db.ForeignKey("shifts.id", ondelete="SET NULL"),
        nullable=True,
    )
    amount     = db.Column(db.Float, nullable=False)
    method     = db.Column(db.Enum(PaymentMethod), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )
    comment    = db.Column(db.String(255), nullable=True)

    # ---------- relationships ---------- #
    client = db.relationship("Client", back_populates="payments", lazy="joined")
    shift  = db.relationship("Shift",  back_populates="payments", lazy="joined")

    # ---------- validation ---------- #
    @validates("amount")
    def validate_amount(self, key, value: float) -> float:
        if value <= 0:
            raise ValueError("Сумма платежа должна быть положительной")
        return round(value, 2)  # фиксируем до сотых

    # ---------- helpers ---------- #
    def __repr__(self) -> str:
        return (
            f"<Payment #{self.id} {self.amount:.2f} {self.method.value} "
            f"client={self.client_id} shift={self.shift_id}>"
        )
