# models/booking.py
from datetime import datetime, timedelta
from enum import Enum

from sqlalchemy import Index, CheckConstraint
from . import db


class BookingStatus(str, Enum):
    ACTIVE     = "active"
    COMPLETED  = "completed"
    CANCELLED  = "cancelled"
    EXPIRED    = "expired"


class Booking(db.Model):
    __tablename__ = "bookings"
    __table_args__ = (
        # быстрый поиск свободных слотов в зоне
        Index("ix_bookings_zone_start", "zone_id", "start_time"),
        # защита от отрицательных и нулевых длительностей
        CheckConstraint("duration > 0", name="ck_booking_positive_duration"),
    )

    id         = db.Column(db.Integer, primary_key=True)
    client_id  = db.Column(
        db.Integer,
        db.ForeignKey("clients.id", ondelete="CASCADE"),
        nullable=False,
    )
    zone_id    = db.Column(
        db.Integer,
        db.ForeignKey("zones.id", ondelete="CASCADE"),
        nullable=False,
    )
    num_pcs    = db.Column(db.Integer, nullable=False)      # сколько машин бронируют
    start_time = db.Column(db.DateTime, nullable=False)
    duration   = db.Column(db.Integer, nullable=False)      # в минутах
    status     = db.Column(
        db.Enum(BookingStatus),
        default=BookingStatus.ACTIVE,
        nullable=False,
    )
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    # ---------- relationships ---------- #
    client = db.relationship("Client", back_populates="bookings", lazy="joined")
    zone   = db.relationship("Zone",   back_populates="bookings", lazy="joined")

    # ---------- convenience helpers ---------- #
    @property
    def end_time(self) -> datetime:
        """Финиш бронирования без лишних подсчётов в сервисах."""
        return self.start_time + timedelta(minutes=self.duration)

    def __repr__(self) -> str:
        return (
            f"<Booking #{self.id} client={self.client_id} zone={self.zone_id} "
            f"{self.start_time:%Y-%m-%d %H:%M}→{self.end_time:%H:%M} "
            f"pcs={self.num_pcs} status={self.status.value}>"
        )
