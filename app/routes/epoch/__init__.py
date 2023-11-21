from flask import Blueprint

bp = Blueprint("epoch", __name__)
from app.routes.epoch import routes
