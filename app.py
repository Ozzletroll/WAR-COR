import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()


# Application factory
def create_app(database_uri='sqlite:///war_cor.db', test_config=None):
    # Create and configure instance of the Flask app
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

    # Initialise login manager
    login_manager = LoginManager()
    login_manager.init_app(app)

    from user import bp as user_bp
    app.register_blueprint(user_bp)

    # User loader callback
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(models.User, user_id)

    return app




