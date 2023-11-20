from flask import Blueprint

bp = Blueprint("test", __name__)
from warcor.routes.test import routes
