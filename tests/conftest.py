import pytest
from app import create_app


@pytest.fixture()
def app():
    app = create_app(database_uri="sqlite:///test.db")
    yield app


@pytest.fixture()
def client(app):
    # app.config['WTF_CSRF_ENABLED'] = False
    app.config["TESTING"] = True
    app.config['SECRET_KEY'] = "TESTING_KEY"
    app.config['WTF_CSRF_ENABLED'] = False
    with app.test_client() as client:
        yield client
