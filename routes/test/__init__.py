from flask import Blueprint

bp = Blueprint("test", __name__)
from routes.test import routes
