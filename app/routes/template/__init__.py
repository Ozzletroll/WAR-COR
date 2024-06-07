from flask import Blueprint

bp = Blueprint("template", __name__)
from app.routes.template import routes
