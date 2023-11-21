from flask import Blueprint

bp = Blueprint("membership", __name__)
from app.routes.membership import routes
