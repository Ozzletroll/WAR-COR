from flask import render_template
from routes.home import bp

#   =======================================
#                  HOMEPAGE
#   =======================================


# Main page
@bp.route("/")
def home():
    return render_template("index.html")
