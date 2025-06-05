# models/role.py
from datetime import datetime
from enum import Enum

from sqlalchemy import Index
from . import db


class SystemRole(str, Enum):
    ADMIN      = "admin"
    OPERATOR   = "operator"
    MANAGER    = "manager"
    TEACHER    = "teacher"
    STUDENT    = "student"
    GUEST      = "guest"


class Role(db.Model):
    __tablename__ = "roles"
    __table_args__ = (
        Index("ix_roles_name", "name"),  # быстрый поиск
    )

    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.Enum(SystemRole), unique=True, nullable=False)
    description = db.Column(db.String(120), nullable=True)
    permissions = db.Column(db.JSON, nullable=True)  # опционально: granulated RBAC

    created_at  = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at  = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    # -------- relationships -------- #
    users = db.relationship(
        "User",
        back_populates="role",
        lazy="dynamic",
        cascade="all, delete-orphan",
    )

    # -------- helpers -------- #
    def __repr__(self) -> str:
        return f"<Role #{self.id} {self.name.value}>"
