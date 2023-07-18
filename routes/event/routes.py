from flask import render_template, redirect, request, url_for, session, flash
from sqlalchemy import select
from flask_login import login_required, current_user
from datetime import datetime

import forms
import models
import auth
import utils.organisers as organisers

from app import db
from routes.event import bp

#   =======================================
#                  Event
#   =======================================


# View event
@bp.route("/campaigns/<campaign_name>/events/<event_name>")
def view_event(campaign_name, event_name):
    target_event_id = request.args["event_id"]
    event = db.session.execute(select(models.Event).filter_by(id=target_event_id)).scalar()

    return render_template("event.html", event=event)


# Add new event
@bp.route("/campaigns/<campaign_name>/events/new_event", methods=["GET", "POST"])
@login_required
def add_event(campaign_name):

    target_campaign_id = request.args["campaign_id"]

    campaign = db.session.execute(select(models.Campaign).filter_by(title=campaign_name, id=target_campaign_id)).scalar()

    auth.permission_required(campaign)

    # Check if date argument given
    if "date" in request.args:
        # Create placeholder event to prepopulate form
        event = models.Event()
        event.title = ""
        event.type = ""
        datestring = request.args["date"]

        args = request.args
        # Increase the date by one unit and format the datestring
        datestring = organisers.format_event_datestring(datestring, args)

        # Populate new form with updated date string
        event.date = datestring
        event.body = ""
        
        form = forms.CreateEventForm(obj=event)

    # Otherwise, create default empty form
    else:
        form = forms.CreateEventForm()

    # Check if user has submitted a new event
    if form.validate_on_submit():
        # Create new event object using form data
        event = models.Event()
        event.title = request.form["title"]
        event.type = request.form["type"]
        event.date = request.form["date"]
        event.location = request.form["location"]
        event.belligerents = request.form["belligerents"]
        event.body = request.form["body"]
        event.result = request.form["result"]

        event.parent_campaign = campaign
        event.parent_campaign.last_edited = datetime.now()

        # Add event to database
        db.session.add(event)
        db.session.commit()

        scroll_target = f"event-{event.id}"

        return redirect(url_for("campaign.edit_timeline",
                                campaign_name=campaign.title,
                                campaign_id=campaign.id,
                                scroll_target=scroll_target))

    # Flash form errors
    for field_name, errors in form.errors.items():
        for error_message in errors:
            flash(field_name + ": " + error_message)

    return render_template("new_event.html", form=form, campaign=campaign)



# Edit existing event
@bp.route("/campaigns/<campaign_name>/events/<event_name>/edit", methods=["GET", "POST"])
@login_required
def edit_event(campaign_name, event_name):
    target_campaign_id = session.get("campaign_id", None)
    target_event_id = session.get("event_id", None)

    campaign = db.session.execute(select(models.Campaign).filter_by(id=target_campaign_id)).scalar()
    event = db.session.execute(select(models.Event).filter_by(id=target_event_id)).scalar()

    # Check if the user has permissions to edit the target campaign.
    auth.permission_required(campaign)

    form = forms.CreateEventForm(obj=event)

    if form.validate_on_submit():
        # Update event object using form data
        event.title = request.form["title"]
        event.type = request.form["type"]
        event.date = request.form["date"]
        event.location = request.form["location"]
        event.belligerents = request.form["belligerents"]
        event.body = request.form["body"]
        event.result = request.form["result"]

        event.parent_campaign.last_edited = datetime.now()

        # Update the database
        db.session.add(event)
        db.session.commit()

        return redirect(url_for("event.view_event",
                                campaign_name=campaign_name,
                                event_name=event.title))

    return render_template("edit_event.html",
                            campaign_name=campaign_name,
                            event_name=event_name)


# Delete existing event
@bp.route("/campaigns/<campaign_name>/events/<event_name>/delete", methods=["GET"])
@login_required
def delete_event(campaign_name, event_name):
    target_campaign_id = session.get("campaign_id", None)
    target_event_id = session.get("event_id", None)

    campaign = db.session.execute(select(models.Campaign).filter_by(id=target_campaign_id)).scalar()
    event = db.session.execute(select(models.Event).filter_by(id=target_event_id)).scalar()

    # Check if the user has permissions to edit the target campaign.
    auth.permission_required(campaign)

    campaign.last_edited = datetime.now()

    db.session.delete(event)
    db.session.commit()

    return redirect(url_for("campaign.show_timeline", campaign_name=campaign_name))
