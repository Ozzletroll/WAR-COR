from flask import Blueprint

bp = Blueprint("session", __name__)
from warcor.routes.session import routes
