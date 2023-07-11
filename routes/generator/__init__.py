from flask import Blueprint

bp = Blueprint("generator", __name__)
from routes.generator import routes
