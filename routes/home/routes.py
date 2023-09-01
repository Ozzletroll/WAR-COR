from flask import render_template
import datetime
from routes.home import bp

#   =======================================
#                  HOMEPAGE
#   =======================================


# Main page
@bp.route("/")
def home():

    # Get year for page footer
    date = datetime.date.today()
    year = date.year

    return render_template("index.html", year=year)
