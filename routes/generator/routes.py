from flask import jsonify, make_response

from routes.generator import bp


#   =======================================
#                Generators
#   =======================================

@bp.route("/generators/random_event")
def random_event_title():
    """View which generates a random event title"""

    result = "Event Title Goes Here"

    response = make_response(result, 200)

    return response
