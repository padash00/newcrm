# models/client.py
from datetime import datetime
from sqlalchemy import Index, CheckConstraint, event
from sqlalchemy.orm import validates

from . import db


class Client(db.Model):
    __tablename__ = "clients"
    __table_args__ = (
        # поиск клиента по телефону моментальный
        Index("ix_clients_phone", "phone"),
        # баланс ≥ 0, долг ≥ 0  (логика: отрицательных не бывает)
        CheckConstraint("balance >= 0", name="ck_client_balance_positive"),
        CheckConstraint("debt    >= 0", name="ck_client_debt_positive"),
    )

    id         = db.Column(db.Integer, primary_key=True)
    full_name  = db.Column(db.String(120), nullable=False)
    phone      = db.Column(db.String(20), unique=True, nullable=True)
    balance    = db.Column(db.Float, default=0.0, nullable=False)
    debt       = db.Column(db.Float, default=0.0, nullable=False)
    notes      = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    # ---------- relationships ---------- #
    bookings = db.relationship(
        "Booking",
        back_populates="client",
        lazy="dynamic",
        cascade="all, delete-orphan",
    )
    sessions = db.relationship(
        "Session",
        back_populates="client",
        lazy="dynamic",
        cascade="all, delete-orphan",
    )
    payments = db.relationship(
        "Payment",
        back_populates="client",
        lazy="dynamic",
        cascade="all, delete-orphan",
    )

    # ---------- validation ---------- #
    @validates("phone")
    def normalize_phone(self, key, value: str | None) -> str | None:
        """+7 (777) 123-45-67 → 7771234567  — храним только цифры для надёжного поиска."""
        if value:
            digits = "".join(filter(str.isdigit, value))
            if len(digits) < 7:  # банальный sanity-check
                raise ValueError("Номер телефона слишком короткий")
            return digits
        return value

    # ---------- helpers ---------- #
    def __repr__(self) -> str:
        return (
            f"<Client #{self.id} {self.full_name} "
            f"balance={self.balance:.2f} debt={self.debt:.2f}>"
        )
