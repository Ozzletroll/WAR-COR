from flask import Blueprint

bp = Blueprint("session", __name__)
from app.routes.session import routes
