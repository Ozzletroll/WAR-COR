from flask import render_template
import datetime
from app.routes.home import bp

#   =======================================
#                   HOME
#   =======================================


# Main page
@bp.route("/")
def home():
    date = datetime.date.today()
    year = date.year

    return render_template("pages/index.html", year=year)


@bp.route("/about")
def about():
    return render_template("pages/about.html")


@bp.route("/contact")
def contact():
    return render_template("pages/contact.html")


@bp.route("/cookie-policy")
def cookie_policy():
    return render_template("pages/cookie_policy.html")
