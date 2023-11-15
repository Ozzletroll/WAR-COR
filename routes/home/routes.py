from flask import render_template
import datetime
from routes.home import bp

#   =======================================
#                   HOME
#   =======================================


# Main page
@bp.route("/")
def home():
    # Get year for page footer
    date = datetime.date.today()
    year = date.year

    return render_template("index.html", year=year)


@bp.route("/about")
def about():
    return render_template("about.html")


@bp.route("/contact")
def contact():
    return render_template("contact.html")


@bp.route("/cookie-policy")
def cookie_policy():

    return render_template("cookie_policy.html")
