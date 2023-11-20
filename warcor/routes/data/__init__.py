from flask import Blueprint

bp = Blueprint("data", __name__)
from warcor.routes.data import routes
