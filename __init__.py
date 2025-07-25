from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "main.login"

def create_app():
    app = Flask(__name__, static_folder='static')  # Εδώ ορίζουμε σωστά το static folder
    app.config['SECRET_KEY'] = "12312312312312312313"  # ΠΡΟΣΘΗΚΗ ΑΥΤΟΥ
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)
    login_manager.init_app(app)

    from app.routes import main
    app.register_blueprint(main)

    return app