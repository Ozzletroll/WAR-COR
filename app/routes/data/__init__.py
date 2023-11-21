from flask import Blueprint

bp = Blueprint("data", __name__)
from app.routes.data import routes
