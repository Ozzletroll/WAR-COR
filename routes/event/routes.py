from flask import render_template, redirect, request, url_for, session, flash
from sqlalchemy import select
from flask_login import login_required, current_user
from datetime import datetime

import forms
import models
import auth
import utils.organisers as organisers
import utils.messengers as messengers

from app import db
from routes.event import bp

#   =======================================
#                  Event
#   =======================================


# View event
@bp.route("/campaigns/<campaign_name>/events/<event_name>", methods=["GET", "POST"])
def view_event(campaign_name, event_name):
    target_event_id = request.args["event_id"]
    event = db.session.execute(select(models.Event).filter_by(id=target_event_id)).scalar()
    campaign = event.parent_campaign

    # Format belligerents data
    belligerents = organisers.separate_belligerents(event.belligerents) 

    form = forms.CommentForm()

    # Set scroll_to target for back button
    scroll_target = f"event-{event.id}"

    # Check if new comment submitted
    if form.validate_on_submit():
        
        # Check user is a member of the campaign
        auth.check_membership(campaign)

        # Create new comment
        comment = models.Comment()
        comment.body = request.form["body"]
        comment.author = current_user
        comment.date = datetime.now()
        comment.parent_event = event
        comment.new = True

        # Add to db
        db.session.add(comment)
        db.session.commit()

        # Create new comment notification
        messengers.send_comment_notification(sender=current_user,
                                             recipients=campaign.members,
                                             campaign=campaign,
                                             event=event)

        return redirect(url_for('event.view_event', 
                                campaign_name=campaign.title, 
                                event_name=event.title, 
                                event_id=event.id,
                                scroll_target=scroll_target))

    return render_template("event.html", 
                           event=event, 
                           campaign=campaign, 
                           belligerents=belligerents,
                           form=form,
                           scroll_target=scroll_target)


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

        if form.header.data:
            event.header = True
        else:
            event.header = False    

        event.parent_campaign = campaign
        event.parent_campaign.last_edited = datetime.now()

        # Add event to database
        db.session.add(event)
        db.session.commit()

        # Update campaigns epochs
        for epoch in campaign.epochs:
            epoch.events.clear()
            epoch.events = organisers.populate_epoch(epoch=epoch, campaign=campaign)
            db.session.commit()
        
        # Create notification message
        messengers.send_event_notification(current_user,
                                           recipients=campaign.members,
                                           campaign=campaign,
                                           event=event)

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
    target_campaign_id = request.args["campaign_id"]
    target_event_id = request.args["event_id"]

    campaign = db.session.execute(select(models.Campaign).filter_by(id=target_campaign_id)).scalar()
    event = db.session.execute(select(models.Event).filter_by(id=target_event_id)).scalar()

    # Create scroll target for back button
    scroll_target = f"event-{event.id}"

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

        if form.header.data:
            event.header = True
        else:
            event.header = False  

        event.parent_campaign.last_edited = datetime.now()

        # Update the database
        db.session.add(event)
        db.session.commit()

        # Update campaigns epochs
        for epoch in campaign.epochs:
            epoch.events.clear()
            epoch.events = organisers.populate_epoch(epoch=epoch, campaign=campaign)
            db.session.commit()

        return redirect(url_for("campaign.edit_timeline", campaign_name=campaign.title, campaign_id=campaign.id, scroll_target=scroll_target))

    # Change form label to 'update'
    form.submit.label.text = 'Update Event'

    return render_template("edit_event.html",
                            campaign=campaign,
                            campaign_name=campaign.title,
                            event_name=event.title,
                            form=form,
                            scroll_target=scroll_target)


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


# Delete comment
@bp.route("/campaigns/<campaign_name>/events/<event_name>/comments/<comment_id>/delete")
@login_required
def delete_comment(campaign_name, event_name, comment_id):
    
    target_campaign_id = request.args["campaign_id"]
    target_event_id = request.args["event_id"]
    target_comment_id = comment_id

    campaign = db.session.execute(select(models.Campaign).filter_by(id=target_campaign_id)).scalar()
    event = db.session.execute(select(models.Event).filter_by(id=target_event_id)).scalar()
    comment = db.session.execute(select(models.Comment).filter_by(id=target_comment_id)).scalar()

    # Check if it is the comment author who is deleting the comment
    if comment.author == current_user:
        auth.check_membership(campaign)
    else:
        # Check if the user has permissions to edit the target campaign.
        auth.permission_required(campaign)

    # Delete the comment
    db.session.delete(comment)
    db.session.commit()

    return redirect(url_for('event.view_event', campaign_name=campaign.title, event_name=event.title, event_id=event.id))



# Add new epoch
@bp.route("/campaigns/<campaign_name>/epochs/new_epoch", methods=["GET", "POST"])
@login_required
def new_epoch(campaign_name):

    target_campaign_id = request.args["campaign_id"]
    campaign = db.session.execute(select(models.Campaign)
                                  .filter_by(title=campaign_name, 
                                             id=target_campaign_id)).scalar()

    auth.permission_required(campaign)

    # Check if date argument given
    if "date" in request.args:
        # Create placeholder event to prepopulate form
        epoch = models.Epoch()

        epoch.start_date = request.args["date"]
        epoch.end_date = request.args["date"]
        form = forms.CreateEpochForm(obj=epoch)

    # Otherwise, create default empty form
    else:
        form = forms.CreateEpochForm()

    if form.validate_on_submit():

        epoch = models.Epoch()

        epoch.title = request.form["title"]
        epoch.start_date = request.form["start_date"]
        epoch.end_date = request.form["end_date"]
        epoch.description = request.form["description"]

        epoch.parent_campaign = campaign

        # Find events that take place during the epoch
        matching_events = organisers.populate_epoch(epoch=epoch, campaign=campaign)
        for event in matching_events:
            epoch.events.append(event)

        scroll_target = f"event-{epoch.id}"

        db.session.add(epoch)
        db.session.commit()

        return redirect(url_for("campaign.edit_timeline", 
                                campaign_name=campaign.title, 
                                campaign_id=campaign.id, 
                                scroll_target=scroll_target))
    
    # Flash form errors
    for field_name, errors in form.errors.items():
        for error_message in errors:
            flash(field_name + ": " + error_message)

    return render_template("new_epoch.html",
                           campaign=campaign,
                           campaign_name=campaign.title,
                           form=form)
