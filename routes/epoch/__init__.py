from flask import Blueprint

bp = Blueprint("epoch", __name__)
from routes.epoch import routes
