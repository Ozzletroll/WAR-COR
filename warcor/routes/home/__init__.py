from flask import Blueprint

bp = Blueprint("home", __name__)
from warcor.routes.home import routes
