from flask import Blueprint

bp = Blueprint("data", __name__)
from routes.data import routes
