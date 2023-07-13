from flask import jsonify, make_response
from random import randint

from routes.generator import bp
from utils.generators import Generator, create_data

#   =======================================
#                Generators
#   =======================================

@bp.route("/generators/random_event")
def random_event_title():
    """View which generates a random event title"""

    generate = Generator()
    result = generate.random_event_title()
    response = make_response(jsonify({"Result": result}), 200)
    
    return response
