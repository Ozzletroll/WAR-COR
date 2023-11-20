from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from config import Config
import os
import logging
from logging.handlers import SMTPHandler

from warcor.utils.generators import create_data

db = SQLAlchemy()
csrf = CSRFProtect()


# Application factory
def create_app(config_class=Config):
    # Create and configure instance of the Flask app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)

    # Initialise database and import models
    db.init_app(app)
    import warcor.models

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
    from warcor.routes.home import bp as home_bp
    app.register_blueprint(home_bp)

    from warcor.routes.user import bp as user_bp
    app.register_blueprint(user_bp)

    from warcor.routes.campaign import bp as campaign_bp
    app.register_blueprint(campaign_bp)

    from warcor.routes.membership import bp as membership_bp
    app.register_blueprint(membership_bp)

    from warcor.routes.epoch import bp as epoch_bp
    app.register_blueprint(epoch_bp)

    from warcor.routes.event import bp as event_bp
    app.register_blueprint(event_bp)

    from warcor.routes.data import bp as data_bp
    app.register_blueprint(data_bp)

    from warcor.routes.generator import bp as gen_bp
    app.register_blueprint(gen_bp)

    from warcor.routes.search import bp as search_bp
    app.register_blueprint(search_bp)

    from warcor.routes.session import bp as session_bp
    app.register_blueprint(session_bp)

    from warcor.routes.error import bp as error_bp
    app.register_blueprint(error_bp)

    from warcor.routes.test import bp as test_bp
    app.register_blueprint(test_bp)

    # User loader callback
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(warcor.models.User, user_id)
    
    # Disable browser caching
    if app.config["DEBUG"]:
        @app.after_request
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


