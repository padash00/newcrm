# models/computer.py
from datetime import datetime
from enum import Enum

from sqlalchemy import Index
from . import db


class ComputerStatus(str, Enum):
    FREE        = "free"
    IN_USE      = "in_use"
    OFFLINE     = "offline"
    MAINTENANCE = "maintenance"


class Computer(db.Model):
    __tablename__ = "computers"
    __table_args__ = (
        # ускоряем выборку свободных/занятых ПК в зоне
        Index("ix_computers_zone_status", "zone_id", "status"),
    )

    id         = db.Column(db.Integer, primary_key=True)
    zone_id    = db.Column(
        db.Integer,
        db.ForeignKey("zones.id", ondelete="CASCADE"),
        nullable=False,
    )
    name       = db.Column(db.String(50), unique=True, nullable=False)
    status     = db.Column(
        db.Enum(ComputerStatus),
        default=ComputerStatus.FREE,
        nullable=False,
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    # ---------- relationships ---------- #
    zone = db.relationship(
        "Zone",
        back_populates="computers",
        lazy="joined",
    )
    sessions = db.relationship(
        "Session",
        back_populates="computer",
        lazy="dynamic",
        cascade="all, delete-orphan",
    )

    # ---------- helpers ---------- #
    def __repr__(self) -> str:
        return f"<PC #{self.id} {self.name} {self.status.value} zone={self.zone_id}>"
