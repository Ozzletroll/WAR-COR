from flask import Blueprint

bp = Blueprint("campaign", __name__)
from warcor.routes.campaign import routes
