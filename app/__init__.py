from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from config import Config
import os
import logging
from logging.handlers import SMTPHandler

from app.utils.generators import create_data

db = SQLAlchemy()
csrf = CSRFProtect()


# Application factory
def create_app(config_class=Config):

    # Create and configure instance of the Flask app
    flask_app = Flask(__name__, instance_relative_config=True)
    flask_app.config.from_object(config_class)

    # Initialise database and import models
    db.init_app(flask_app)
    import app.models

    # Create the database
    with flask_app.app_context():
        db.create_all()

    # Initialise db migrations
    migrate = Migrate(flask_app, db)

    # Initialise CSRFProtect
    csrf.init_app(flask_app)

    # Initialise login manager
    login_manager = LoginManager()
    login_manager.init_app(flask_app)

    # Set login_required redirect page
    login_manager.login_view = "user.login"
    login_manager.login_message = "Please log in to access this page"

    # Register blueprints
    from app.routes.home import bp as home_bp
    flask_app.register_blueprint(home_bp)

    from app.routes.user import bp as user_bp
    flask_app.register_blueprint(user_bp)

    from app.routes.campaign import bp as campaign_bp
    flask_app.register_blueprint(campaign_bp)

    from app.routes.membership import bp as membership_bp
    flask_app.register_blueprint(membership_bp)

    from app.routes.epoch import bp as epoch_bp
    flask_app.register_blueprint(epoch_bp)

    from app.routes.event import bp as event_bp
    flask_app.register_blueprint(event_bp)

    from app.routes.data import bp as data_bp
    flask_app.register_blueprint(data_bp)

    from app.routes.generator import bp as gen_bp
    flask_app.register_blueprint(gen_bp)

    from app.routes.search import bp as search_bp
    flask_app.register_blueprint(search_bp)

    from app.routes.session import bp as session_bp
    flask_app.register_blueprint(session_bp)

    from app.routes.error import bp as error_bp
    flask_app.register_blueprint(error_bp)

    from app.routes.test import bp as test_bp
    flask_app.register_blueprint(test_bp)

    # User loader callback
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(app.models.User, user_id)
    
    # Disable browser caching
    if flask_app.config["DEBUG"]:
        @flask_app.after_request
        def after_request(response):
            response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
            response.headers["Expires"] = 0
            response.headers["Pragma"] = "no-cache"
            return response

    # os.path.join is used to allow the test config to also access the data
    data_folder = os.path.join(os.path.dirname(__file__), 'utils', 'data')

    # Create data folder if necessary
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)

    # Create data for random name generator
    try:
        with open(os.path.join(data_folder, 'nouns.json'), 'r') as file:
            pass
    except FileNotFoundError:
        create_data()

    try:
        with open(os.path.join(data_folder, 'adjectives.json'), 'r') as file:
            pass
    except FileNotFoundError:
        create_data()    

    try:
        with open(os.path.join(data_folder, 'verbs.json'), 'r') as file:
            pass
    except FileNotFoundError:
        create_data()

    # Configure error logging email
    if not flask_app.debug:
        if flask_app.config['MAIL_SERVER']:
            auth = None
            if flask_app.config['MAIL_USERNAME'] or flask_app.config['MAIL_PASSWORD']:
                auth = (flask_app.config['MAIL_USERNAME'], flask_app.config['MAIL_PASSWORD'])
            secure = None
            if flask_app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(flask_app.config['MAIL_SERVER'], flask_app.config['MAIL_PORT']),
                fromaddr='no-reply@' + flask_app.config['MAIL_SERVER'],
                toaddrs=flask_app.config['ADMINS'], subject='WAR/COR Failure',
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            flask_app.logger.addHandler(mail_handler)

    return flask_app


