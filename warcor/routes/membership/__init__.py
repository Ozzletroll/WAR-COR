from flask import Blueprint

bp = Blueprint("membership", __name__)
from warcor.routes.membership import routes
