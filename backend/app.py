
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
app.register_blueprint(auth_bp)

@app.route('/')
def home():
    return 'CRM для компьютерного клуба — работает!'

if __name__ == '__main__':
    app.run(debug=True)
