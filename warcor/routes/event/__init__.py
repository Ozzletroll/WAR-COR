from flask import Blueprint

bp = Blueprint("event", __name__)
from warcor.routes.event import routes
