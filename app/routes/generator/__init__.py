from flask import Blueprint

bp = Blueprint("generator", __name__)
from app.routes.generator import routes
