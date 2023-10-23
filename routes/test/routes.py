from flask import abort
from routes.test import bp

#   =======================================
#                   TEST
#   =======================================


# Test route for triggering 403 error
@bp.route("/test/restricted_route")
def restricted_route():
    abort(403)


# Test route for triggering 404 error
@bp.route("/test/nonexistent_route")
def nonexistent_route():
    abort(404)


# Test route for triggering 500 error
@bp.route("/test/server_error_route")
def server_error_route():
    abort(500)
