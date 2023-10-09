from flask import Blueprint

bp = Blueprint("errors", __name__)
from routes.error import routes
