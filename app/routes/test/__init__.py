from flask import Blueprint

bp = Blueprint("test", __name__)
from app.routes.test import routes
