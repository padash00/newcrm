from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    full_name = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='operator')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    role_rel = db.relationship('Role', back_populates='users')
    shifts = db.relationship('Shift', back_populates='operator')
    actions = db.relationship('Action', back_populates='user')

    def set_password(self, password: str) -> None:
        """Hash and store the given password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Check the given password against the stored hash."""
        return check_password_hash(self.password_hash, password)
