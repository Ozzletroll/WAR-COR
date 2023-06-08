from flask import Blueprint

bp = Blueprint("home", __name__)
from routes.home import routes
