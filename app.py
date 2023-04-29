import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# Configure Flask app
def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///war_cor.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialise database
    db.init_app(app)
    import models

    with app.app_context():
        db.create_all()

    return app




