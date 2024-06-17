from flask import abort, current_app, redirect, url_for
from functools import wraps
from app.routes.test import bp


#   =======================================
#                   TEST
#   =======================================

def test_config_only(function):
    """ Decorator to prevent access to testing routes outside test config."""
    @wraps(function)
    def decorated_function(*args, **kwargs):
        if not current_app.config["TESTING"]:
            return redirect(url_for('home.home'))
        return function(*args, **kwargs)
    return decorated_function


# Test route for triggering 400 error
@bp.route("/test/bad_request_route")
@test_config_only
def bad_request_route():
    abort(400)


# Test route for triggering 403 error
@bp.route("/test/restricted_route")
@test_config_only
def restricted_route():
    abort(403)


# Test route for triggering 404 error
@bp.route("/test/nonexistent_route")
@test_config_only
def nonexistent_route():
    abort(404)


# Test route for 429 page
@bp.route("/test/too_many_requests_route")
@test_config_only
def too_many_requests_route():
    abort(429)


# Test route for triggering 500 error
@bp.route("/test/server_error_route")
@test_config_only
def server_error_route():
    abort(500)
