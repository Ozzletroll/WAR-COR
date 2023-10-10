from flask import Blueprint

bp = Blueprint("membership", __name__)
from routes.membership import routes
