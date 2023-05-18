import pytest
from app import create_app
from routes import configure_routes


@pytest.fixture()
def app():
    app = create_app(database_uri="sqlite:///test.db")
    configure_routes(app)
    yield app


@pytest.fixture()
def client(app):
    app.config.update({"TESTING": True})
    # app.config['WTF_CSRF_ENABLED'] = False
    app.config['SECRET_KEY'] = "TESTING_KEY"
    app.config['WTF_CSRF_ENABLED'] = False
    with app.test_client() as client:
        yield client
