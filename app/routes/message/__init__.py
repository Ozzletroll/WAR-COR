from flask import Blueprint

bp = Blueprint("message", __name__)
from app.routes.message import routes
