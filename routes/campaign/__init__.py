from flask import Blueprint

bp = Blueprint("campaign", __name__)
from routes.campaign import routes
