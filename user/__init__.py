from flask import Blueprint

bp = Blueprint("user", __name__)
from user import routes
