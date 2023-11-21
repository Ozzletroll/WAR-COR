from flask import Blueprint

bp = Blueprint("campaign", __name__)
from app.routes.campaign import routes
