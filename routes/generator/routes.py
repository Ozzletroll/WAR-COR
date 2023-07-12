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

    generator = Generator()
    result = generator.generate_operation()
    response = make_response(jsonify({"Result": result}), 200)
    
    return response