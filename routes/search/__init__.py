from flask import Blueprint

bp = Blueprint("search", __name__)
from routes.search import routes
