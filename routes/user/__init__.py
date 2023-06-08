from flask import Blueprint

bp = Blueprint("user", __name__)
from routes.user import routes
