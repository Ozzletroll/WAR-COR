import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()


# Application factory
def create_app(database_uri='sqlite:///war_cor.db'):
    app = Flask(__name__, instance_relative_config=True)
    app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialise database and import models
    db.init_app(app)
    import models

    # Create the database
    with app.app_context():
        db.create_all()

    # Login manager
    login_manager = LoginManager()
    login_manager.init_app(app)

    return app




