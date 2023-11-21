from flask import Blueprint

bp = Blueprint("event", __name__)
from app.routes.event import routes
