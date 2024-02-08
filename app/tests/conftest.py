import pytest
import os
from flask import template_rendered
from app import create_app
from app import db
from app.tests.fixtures import *
from config import TestingConfig, TestingPostgresConfig


@pytest.fixture(scope="module")
def app():
    """ 
        Main app fixture for pytest.
        Uses "TEST_DB_TYPE" environment variable to determine
        testing config to pass.
        
    """
    if os.environ["TESTING_USE_POSTGRESQL"]:
        app = create_app(config_class=TestingPostgresConfig)
    else:
        app = create_app(config_class=TestingConfig)
    yield app

    # Teardown
    with app.app_context():
        db.session.close()
        db.drop_all()


@pytest.fixture()
def client(app):
    with app.test_client() as client:
        yield client


@pytest.fixture()
def auth(client):
    return AuthActions(client)


@pytest.fixture()
def campaign(client):
    return CampaignActions(client)


@pytest.fixture()
def event(client):
    return EventActions(client)


@pytest.fixture()
def epoch(client):
    return EpochActions(client)


@pytest.fixture
def captured_templates(app):
    """ Captures the template and context of the app.
        Pass the fixture to the test function, and the
        templates and contexts can be accessed with:

        template, context = captured_templates[index]
    """

    recorded = []

    def record(sender, template, context, **extra):
        recorded.append((template, context))

    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)
