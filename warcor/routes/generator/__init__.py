from flask import Blueprint

bp = Blueprint("generator", __name__)
from warcor.routes.generator import routes
