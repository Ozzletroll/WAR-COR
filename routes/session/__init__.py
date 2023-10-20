from flask import Blueprint

bp = Blueprint("session", __name__)
from routes.session import routes
