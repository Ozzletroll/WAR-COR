from flask import Blueprint

bp = Blueprint("user", __name__)
from warcor.routes.user import routes
