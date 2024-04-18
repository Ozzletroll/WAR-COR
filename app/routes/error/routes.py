from flask import render_template, redirect, url_for, flash
from app import db

from app.routes.error import bp


@bp.app_errorhandler(401)
def access_denied_error(error):
    flash("Please log in to access this page")
    return redirect(url_for("user.login"))


@bp.app_errorhandler(403)
def access_denied_error(error):
    return render_template("pages/error.html", error=error), 403


@bp.app_errorhandler(404)
def not_found_error(error):
    return render_template("pages/error.html", error=error), 404


@bp.app_errorhandler(429)
def too_many_requests_error(error):
    return render_template("pages/error.html", error=error), 429


@bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template("pages/error.html", error=error), 500
