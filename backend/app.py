
from flask_cors import CORS
import os
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'SQLALCHEMY_DATABASE_URI', 'sqlite:///club.db'
)
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'change-me')
CORS(app, origins=[o.strip() for o in os.environ.get('CORS_ORIGINS', 'http://localhost:3000').split(',')])
from flask_jwt_extended import JWTManager
from models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///club.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'change-me'
db.init_app(app)
jwt = JWTManager(app)

from routes.auth import auth_bp
from routes.clients import clients_bp
from routes.shifts import shifts_bp
from routes.sessions import sessions_bp
from routes.cash import cash_bp
from routes.zones import zones_bp
from routes.computers import computers_bp
from routes.tariffs import tariffs_bp
from routes.promotions import promos_bp
from routes.bookings import bookings_bp
from routes.reports import reports_bp

app.register_blueprint(auth_bp)
app.register_blueprint(clients_bp)
app.register_blueprint(shifts_bp)
app.register_blueprint(sessions_bp)
app.register_blueprint(cash_bp)
app.register_blueprint(zones_bp)
app.register_blueprint(computers_bp)
app.register_blueprint(tariffs_bp)
app.register_blueprint(promos_bp)
app.register_blueprint(bookings_bp)
app.register_blueprint(reports_bp)
=======
from flask import Flask
from flask_jwt_extended import JWTManager
from models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///club.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'change-me'
db.init_app(app)
jwt = JWTManager(app)

from routes.auth import auth_bp
codex-ui-clean
from routes.clients import clients_bp
from routes.shifts import shifts_bp
from routes.sessions import sessions_bp
from routes.cash import cash_bp
from routes.zones import zones_bp
from routes.computers import computers_bp
from routes.tariffs import tariffs_bp
from routes.promotions import promos_bp
from routes.bookings import bookings_bp

app.register_blueprint(auth_bp)
app.register_blueprint(clients_bp)
app.register_blueprint(shifts_bp)
app.register_blueprint(sessions_bp)
app.register_blueprint(cash_bp)
app.register_blueprint(zones_bp)
app.register_blueprint(computers_bp)
app.register_blueprint(tariffs_bp)
app.register_blueprint(promos_bp)
app.register_blueprint(bookings_bp)

app.register_blueprint(auth_bp)
main
main

@app.route('/')
def home():
    return 'CRM для компьютерного клуба — работает!'

if __name__ == '__main__':
    app.run(debug=True)
