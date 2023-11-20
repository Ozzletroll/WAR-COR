from flask import Blueprint

bp = Blueprint("errors", __name__)
from warcor.routes.error import routes

