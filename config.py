import os
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor


class Config(object):
    # Flask
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = "sqlite:///war_cor.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    # Mailersender
    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = int(os.environ.get("MAIL_PORT") or 25)
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS") is not None
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    ADMIN = os.environ.get("ADMIN")
    # APScheduler
    SCHEDULER_JOBSTORES = {
        "default": SQLAlchemyJobStore(url="sqlite:///instance/war_cor.db")
    }
    SCHEDULER_EXECUTORS = {
        "default": ThreadPoolExecutor(max_workers=4),
    }
    SCHEDULER_JOB_DEFAULTS = {
        "coalesce": False,
        "max_instances": 3
    }
    SCHEDULER_TIMEZONE = "UTC"
    # Flask-APScheduler
    SCHEDULER_API_ENABLED = False


class TestingConfig(Config):
    TESTING = True
    SECRET_KEY = "Testing_Secret_Key"
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"
    WTF_CSRF_ENABLED = False
    SCHEDULER_JOBSTORES = {
        "default": SQLAlchemyJobStore(url="sqlite:///instance/test.db")
    }


class TestingPostgresConfig(TestingConfig):
    SQLALCHEMY_DATABASE_URI = os.environ.get("POSTGRESQL_DATABASE_URI")
    SCHEDULER_JOBSTORES = {
        "default": SQLAlchemyJobStore(url=os.environ.get("POSTGRESQL_DATABASE_URI"))
    }


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("POSTGRESQL_DATABASE_URI")
    SCHEDULER_JOBSTORES = {
        "default": SQLAlchemyJobStore(url=os.environ.get("POSTGRESQL_DATABASE_URI"))
    }
