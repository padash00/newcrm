# models/action.py
from datetime import datetime
from enum import Enum

from sqlalchemy import Index
from . import db


class ActionType(str, Enum):
    LOGIN     = "login"
    LOGOUT    = "logout"
    CREATE    = "create"
    UPDATE    = "update"
    DELETE    = "delete"


class Action(db.Model):
    __tablename__ = "actions"
    __table_args__ = (
        # быстрый поиск действий конкретного пользователя по дате
        Index("ix_actions_user_date", "user_id", "created_at"),
    )

    id          = db.Column(db.Integer, primary_key=True)
    user_id     = db.Column(db.Integer,
                            db.ForeignKey("users.id", ondelete="CASCADE"),
                            nullable=False)
    action_type = db.Column(db.Enum(ActionType), nullable=False)
    details     = db.Column(db.Text, nullable=True)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # -------- relationships -------- #
    user = db.relationship(
        "User",
        back_populates="actions",
        lazy="joined"       # сразу тянем пользователя; экономим второй запрос
    )

    # -------- dunder helpers -------- #
    def __repr__(self) -> str:
        return (
            f"<Action #{self.id} {self.action_type.value} "
            f"by user={self.user_id} at {self.created_at:%Y-%m-%d %H:%M:%S}>"
        )
