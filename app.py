from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_ckeditor import CKEditor
from flask_wtf.csrf import CSRFProtect
import os
import logging
from logging.handlers import SMTPHandler

from utils.generators import create_data

db = SQLAlchemy()
csrf = CSRFProtect()
ckeditor = CKEditor()

# Application factory
def create_app(database_uri='sqlite:///war_cor.db', test_config=None):
    # Create and configure instance of the Flask app
    app = Flask(__name__, instance_relative_config=True)
    app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = "Lax"
    app.config['CKEDITOR_SERVE_LOCAL'] = True
    app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
    app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT') or 25)
    app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS') is not None
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
    app.config['ADMINS'] = ["admin-email-goes-here"]

    # Initialise database and import models
    db.init_app(app)
    import models

    # Create the database
    with app.app_context():
        db.create_all()

    # Initialise db migrations
    migrate = Migrate(app, db)

    # Initialise CSRFProtect
    csrf.init_app(app)

    # Initialise login manager
    login_manager = LoginManager()
    login_manager.init_app(app)

    # Set login_required redirect page
    login_manager.login_view = "user.login"
    login_manager.login_message = "Please log in to access this page"

    # Register blueprints
    from routes.home import bp as home_bp
    app.register_blueprint(home_bp)

    from routes.user import bp as user_bp
    app.register_blueprint(user_bp)

    from routes.campaign import bp as campaign_bp
    app.register_blueprint(campaign_bp)

    from routes.epoch import bp as epoch_bp
    app.register_blueprint(epoch_bp)

    from routes.event import bp as event_bp
    app.register_blueprint(event_bp)

    from routes.data import bp as data_bp
    app.register_blueprint(data_bp)

    from routes.generator import bp as gen_bp
    app.register_blueprint(gen_bp)

    from routes.error import bp as error_bp
    app.register_blueprint(error_bp)

    # User loader callback
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(models.User, user_id)
    
    # Disable browser caching
    if app.config["DEBUG"]:
        @app.after_request
        def after_request(response):
            response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
            response.headers["Expires"] = 0
            response.headers["Pragma"] = "no-cache"
            return response

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

    # Configure error logging email
    if not app.debug:
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'], subject='WAR/COR Failure',
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

    return app



