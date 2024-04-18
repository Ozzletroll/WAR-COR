from flask import jsonify, make_response

from app.routes.generator import bp
from app.utils.generators import Generator


#   =======================================
#                Generators
#   =======================================

@bp.route("/generate/random-event-title")
def random_event_title():
    generate = Generator()
    result = generate.random_event_title()
    response = make_response(jsonify({"Result": result}), 200)
    
    return response
