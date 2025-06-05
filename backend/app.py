import os
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from models import db

def create_app() -> Flask:
    app = Flask(__name__)

    app.config.update(
        SQLALCHEMY_DATABASE_URI=os.getenv(
            "SQLALCHEMY_DATABASE_URI", "sqlite:///club.db"
        ),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        JWT_SECRET_KEY=os.getenv("JWT_SECRET_KEY", "change-me"),
    )

    db.init_app(app)
    JWTManager(app)

    cors_origins = [
        origin.strip()
        for origin in os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
    ]
    CORS(app, origins=cors_origins, supports_credentials=True)

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

    blueprints = [
        auth_bp,
        clients_bp,
        shifts_bp,
        sessions_bp,
        cash_bp,
        zones_bp,
        computers_bp,
        tariffs_bp,
        promos_bp,
        bookings_bp,
        reports_bp,
    ]
    for bp in blueprints:
        app.register_blueprint(bp)
    @app.route("/")
    def healthcheck():
        return "CRM для компьютерного клуба — работает!", 200

    return app
if __name__ == "__main__":
    # Запуск для локальной разработки (`python app.py`)
    _app = create_app()
    _app.run(host="0.0.0.0", port=8000, debug=True)
