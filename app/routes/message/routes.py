from flask import redirect, request, url_for, make_response, jsonify
from flask_login import login_required, current_user

from app import db, models
from app.routes.message import bp


# Function called when viewing/dismissing a notification
@bp.route("/user/messages/dismiss", methods=["POST"])
@login_required
def dismiss_message():

    message_id = request.form["message_id"]

    message = (db.session.query(models.Message)
               .filter(models.Message.id == message_id)
               .first_or_404(description="No matching message found"))

    # If redirecting to event, build url prior to potential message deletion
    view = request.args.get("view", None)

    if view and hasattr(message, "target_event"):
        event_url = url_for("event.view_event",
                            campaign_name=message.target_campaign.url_title,
                            campaign_id=message.target_campaign.id,
                            event_name=message.target_event.url_title,
                            event_id=message.target_event.id)

    message.dismiss(current_user)

    if view:
        return redirect(event_url)
    else:   
        response = make_response(jsonify({"Message": "Message dismissed"}), 200)
        return response


# Function called when dismissing all messages
@bp.route("/user/messages/dismiss-all", methods=["POST"])
@login_required
def dismiss_all():

    messages = current_user.messages.copy()

    for message in messages:
        message.dismiss(current_user)
     
    response = make_response(jsonify({"Message": "All messages dismissed"}), 200)
    return response
