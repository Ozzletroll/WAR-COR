from flask import Blueprint

bp = Blueprint("event", __name__)
from routes.event import routes
