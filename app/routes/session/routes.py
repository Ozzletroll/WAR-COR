from flask import current_app, url_for, session, jsonify, make_response, request, redirect
from flask_login import current_user
from datetime import timedelta
from app import limiter

from app.routes.session import bp


#   =======================================
#                 SESSION
#   =======================================

@bp.app_context_processor
def check_consent():
    """ Checks for GDPR consent form acceptance cookie, and
        injects variable to templates. """

    excluded_routes = ["/", "/about", "/contact", "/cookie-policy"]

    if request.path not in excluded_routes:
        
        if not request.cookies.get("warcor_consent") and current_app.config["DEBUG"] == False:
            return dict(consent=False)
        else:
            return dict(consent=True)
        
    else:
        return dict(consent=True)
    

@bp.route("/session/accept_cookies", methods=["POST"])
def accept_cookies():
    """ Sets the consent form acceptance cookie. Called via fetch request from consent form
        component.  """

    expiry = int(timedelta(days=30).total_seconds())
    response = make_response(redirect(request.referrer))
    response.set_cookie("warcor_consent", 
                        "True", 
                        secure=True, 
                        max_age=expiry,
                        samesite="Strict")

    return response


# Get and clear campaign page scroll target session variable
@bp.route("/session/campaign-scroll-target", methods=["GET"])
def campaign_target():

    if "campaign_scroll_target" in session:

        response_data = {"Message": "Session variable cleared",
                         "type": "element", 
                         "target": session["campaign_scroll_target"]}
        # Clear session variable
        session.pop("campaign_scroll_target", None)
        response = make_response(jsonify(response_data), 200)

    else:
        response = make_response(jsonify({"Message": "Session variable not set"}), 204)

    return response
    

# Get and clear timeline page scroll target session variable
@bp.route("/session/timeline-scroll-target", methods=["GET"])
def timeline_target():

    if "timeline_relative_scroll" in session:
        response_data = {"Message": "Session variable cleared", 
                         "type": "relative",
                         "target": session["timeline_relative_scroll"]}
        # Clear session variable
        session.pop("timeline_relative_scroll", None)
        response = make_response(jsonify(response_data), 200)

    elif "timeline_scroll_target" in session:

        response_data = {"Message": "Session variable cleared",
                         "type": "element", 
                         "target": session["timeline_scroll_target"]}
        # Clear session variable
        session.pop("timeline_scroll_target", None)
        response = make_response(jsonify(response_data), 200)

    else:
        response = make_response({"Message": "Session variable not set"}, 204)

    return response


# Set scroll target when changing between editing and viewing timeline layer
@bp.route("/session/timeline-edit-toggle", methods=["POST"])
def timeline_edit_toggle():
    """ This route is called via fetch request when the user clicks
        to toggle between viewing and editing the timeline.
        The target variable is a the id of the element closest
        to where the user left off, which is used by the template
        to scroll to. """

    json_data = request.get_json()
    target = json_data["target"]

    session["timeline_relative_scroll"] = f"{target}"
    response = make_response({"Message": "Session variable set"}, 200)

    return response


# Get and clear event page comment scroll target session variable
@bp.route("/session/comment-scroll-target", methods=["GET"])
def comment_target():

    if "comment_scroll_target" in session:

        response_data = {"Message": "Session variable cleared",
                         "type": "element", 
                         "target": session["comment_scroll_target"]}
        # Clear session variable
        session.pop("comment_scroll_target", None)
        response = make_response(jsonify(response_data), 200)

    else:
        response = make_response({"Message": "Session variable not set"}, 204)

    return response


# Back button route
@bp.route("/back", methods=["GET"])
@limiter.limit("60/minute")
def back():
    """Function to handle redirects for the back button on the user, 
    members and advanced search pages.
    Uses stored "previous_url" session variable if available, otherwise
    users fallback urls."""

    if "previous_url" in session:
        referrer = session["previous_url"]
    elif request.referrer:
        referrer = request.referrer
    elif current_user.is_authenticated:
        referrer = url_for("campaign.campaigns")
    else:
        referrer = url_for("home.home")

    return redirect(referrer)
