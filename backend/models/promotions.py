# models/promotion.py
from datetime import datetime
from enum import Enum

from sqlalchemy import Index, CheckConstraint
from sqlalchemy.orm import validates

from . import db


class DiscountType(str, Enum):
    PERCENT  = "percent"   # 15 %
    FLAT     = "flat"      # −200 тг с часа
    FREE_MIN = "free_min"  # 60 мин в подарок
    BONUS_PC = "bonus_pc"  # 2 + 1 компьютер


class Promotion(db.Model):
    __tablename__ = "promotions"
    __table_args__ = (
        # быстрый поиск действующих акций
        Index("ix_promotions_active_dates", "is_active", "starts_at", "ends_at"),
        CheckConstraint("discount_value > 0", name="ck_promo_discount_positive"),
    )

    id             = db.Column(db.Integer, primary_key=True)
    name           = db.Column(db.String(80), nullable=False, unique=True)

    # что именно нужно для применения (например, «3 ч + 2 бесплатно»)
    pattern        = db.Column(db.String(120), nullable=True)

    discount_type  = db.Column(db.Enum(DiscountType), nullable=False)
    discount_value = db.Column(db.Float, nullable=False)  # %  или  тг / мин

    # когда акция работает
    starts_at      = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    ends_at        = db.Column(db.DateTime, nullable=True)  # None → бессрочно

    # сложные расписания (cron-/rrule-json) — опционально
    schedule       = db.Column(db.JSON, nullable=True)

    is_active      = db.Column(db.Boolean, default=True, nullable=False)

    created_at     = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at     = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    # ---------- validation ---------- #
    @validates("discount_value")
    def validate_value(self, key, value: float) -> float:
        if value <= 0:
            raise ValueError("discount_value должен быть > 0")
        return round(value, 2)

    @validates("ends_at")
    def validate_dates(self, key, value: datetime | None) -> datetime | None:
        if value and value < self.starts_at:
            raise ValueError("ends_at не может быть раньше starts_at")
        return value

    # ---------- helpers ---------- #
    def is_current(self) -> bool:
        """Действует ли акция прямо сейчас — учитывая дату и флаг is_active."""
        now = datetime.utcnow()
        return (
            self.is_active
            and self.starts_at <= now
            and (self.ends_at is None or now <= self.ends_at)
        )

    def __repr__(self) -> str:
        return (
            f"<Promo #{self.id} {self.name} {self.discount_type.value}:"
            f"{self.discount_value} active={self.is_current()}>"
        )
