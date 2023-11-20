from flask import jsonify, make_response

from warcor.routes.generator import bp
from warcor.utils.generators import Generator


#   =======================================
#                Generators
#   =======================================

@bp.route("/generate/random-event-title")
def random_event_title():
    """View which generates a random event title"""

    generate = Generator()
    result = generate.random_event_title()
    response = make_response(jsonify({"Result": result}), 200)
    
    return response
