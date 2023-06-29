from flask import render_template, redirect, request, url_for, session
from sqlalchemy import select
from flask_login import login_required, current_user
from datetime import datetime

import forms
import models

from app import db
from routes.event import bp

#   =======================================
#                  Event
#   =======================================


# View event
@bp.route("/campaigns/<campaign_name>/<event_name>")
def view_event(campaign_name, event_name):
    target_event_id = session.get("event_id", None)
    event = db.session.execute(select(models.Event).filter_by(id=target_event_id)).scalar()

    return render_template("event.html", event=event)


# Add new event
@bp.route("/campaigns/<campaign_name>/new_event", methods=["GET", "POST"])
@login_required
def add_event(campaign_name):

    target_campaign_id = request.args["campaign_id"]

    campaign = db.session.execute(select(models.Campaign).filter_by(title=campaign_name, id=target_campaign_id)).scalar()

    # Check if the user has permissions to edit the target campaign.
    if campaign in current_user.permissions:

        form = forms.CreateEventForm()

        # Check if user has submitted a new event
        if form.validate_on_submit():
            # Create new event object using form data
            event = models.Event()
            event.title = request.form["title"]
            event.type = request.form["type"]

            # Convert date to datetime object
            date = request.form["date"]
            date_format = '%Y-%m-%d %H:%M:%S'
            date_obj = datetime.strptime(date, date_format)
            event.date = date_obj

            event.location = request.form["location"]
            event.belligerents = request.form["belligerents"]
            event.body = request.form["body"]
            event.result = request.form["result"]

            event.parent_campaign = campaign

            # Add event to database
            db.session.add(event)
            db.session.commit()

            return redirect(url_for("campaign.show_timeline",
                                    campaign_name=campaign.title,
                                    campaign_id=campaign.id))

        return render_template("new_event.html", form=form, campaign=campaign)

    else:
        # Redirect to homepage if the user is somehow trying to edit a campaign that they
        # do not have permission for.
        return redirect(url_for("home.home"))


# Edit existing event
@bp.route("/campaigns/<campaign_name>/<event_name>/edit", methods=["GET", "POST"])
@login_required
def edit_event(campaign_name, event_name):
    target_campaign_id = session.get("campaign_id", None)
    target_event_id = session.get("event_id", None)

    campaign = db.session.execute(select(models.Campaign).filter_by(id=target_campaign_id)).scalar()
    event = db.session.execute(select(models.Event).filter_by(id=target_event_id)).scalar()

    # Check if the user has permissions to edit the target campaign.
    if campaign in current_user.permissions:

        form = forms.CreateEventForm(obj=event)

        if form.validate_on_submit():
            # Update event object using form data
            event.title = request.form["title"]
            event.type = request.form["type"]

            date = request.form["date"]
            # Convert date to datetime object
            date_format = '%Y-%m-%d %H:%M:%S'
            date_obj = datetime.strptime(date, date_format)
            event.date = date_obj

            event.location = request.form["location"]
            event.belligerents = request.form["belligerents"]
            event.body = request.form["body"]
            event.result = request.form["result"]

            # Update the database
            db.session.add(event)
            db.session.commit()

            session["campaign_id"] = target_campaign_id
            session["event_id"] = event.id

            return redirect(url_for("event.view_event",
                                    campaign_name=campaign_name,
                                    event_name=event.title))

        return render_template("edit_event.html",
                               campaign_name=campaign_name,
                               event_name=event_name)

    # Redirect to homepage if the user is somehow trying to edit an event that they
    # do not have permission for.
    return redirect(url_for("home.home"))


# Delete existing event
@bp.route("/campaigns/<campaign_name>/<event_name>/delete", methods=["GET"])
@login_required
def delete_event(campaign_name, event_name):
    target_campaign_id = session.get("campaign_id", None)
    target_event_id = session.get("event_id", None)

    campaign = db.session.execute(select(models.Campaign).filter_by(id=target_campaign_id)).scalar()
    event = db.session.execute(select(models.Event).filter_by(id=target_event_id)).scalar()

    # Check if the user has permissions to edit the target campaign.
    if campaign in current_user.permissions:
        db.session.delete(event)
        db.session.commit()

    return redirect(url_for("campaign.show_timeline", campaign_name=campaign_name))
