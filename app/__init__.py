from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from config import Config

# Initialisation des extensions
db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Connexion des extensions à l'app
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    login_manager.login_view = 'main.connexion'
    login_manager.login_message = 'connectez-vous pour acceder a cette page.'
    login_manager.login_category = 'Warning'

    # Enregistrement des routes
    from app.routes import main
    app.register_blueprint(main)

    return app