from flask import Blueprint

bp = Blueprint("search", __name__)
from app.routes.search import routes
