from flask import Blueprint

bp = Blueprint("epoch", __name__)
from warcor.routes.epoch import routes
