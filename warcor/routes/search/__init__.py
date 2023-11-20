from flask import Blueprint

bp = Blueprint("search", __name__)
from warcor.routes.search import routes
