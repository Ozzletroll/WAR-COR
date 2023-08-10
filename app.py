import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_ckeditor import CKEditor

from utils.generators import create_data

db = SQLAlchemy()
ckeditor = CKEditor()

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

    # Initialise db migrations
    migrate = Migrate(app, db)

    # Initialise login manager
    login_manager = LoginManager()
    login_manager.init_app(app)

    # Register blueprints
    from routes.home import bp as home_bp
    app.register_blueprint(home_bp)

    from routes.user import bp as user_bp
    app.register_blueprint(user_bp)

    from routes.campaign import bp as campaign_bp
    app.register_blueprint(campaign_bp)

    from routes.event import bp as event_bp
    app.register_blueprint(event_bp)

    from routes.data import bp as data_bp
    app.register_blueprint(data_bp)

    from routes.generator import bp as gen_bp
    app.register_blueprint(gen_bp)

    # User loader callback
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(models.User, user_id)

    # Create data for random name generator
    try:
        with open(f"{app.root_path}/utils/data/nouns.json", "r") as file:
            pass
    except FileNotFoundError:
        create_data()

    try:
        with open(f"{app.root_path}/utils/data/adjectives.json", "r") as file:
            pass
    except FileNotFoundError:
        create_data()    

    try:
        with open(f"{app.root_path}/utils/data/verbs.json", "r") as file:
            pass
    except FileNotFoundError:
        create_data()

    # Initialise CKEditor
    ckeditor.init_app(app)

    return app



