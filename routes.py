from flask import render_template, redirect, request, url_for, flash
from sqlalchemy import select
from flask_login import login_user, login_required, current_user, logout_user
import werkzeug
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

import forms
import models

from app import db


# Here all the routes are configured as a function, with an instance of the app passed as a parameter.
def configure_routes(flask_app):

    # User loader callback
    # https://flask-login.readthedocs.io/en/latest/#login-example
    @flask_app.login_manager.user_loader
    def load_user(user_id):
        return db.session.get(models.User, user_id)

    #   =======================================
    #                  HOMEPAGE
    #   =======================================

    # Main page
    @flask_app.route("/")
    def home():
        return render_template("index.html")

    #   =======================================
    #                  User
    #   =======================================

    # New user registration
    @flask_app.route("/register", methods=["GET", "POST"])
    def register():

        form = forms.RegisterUserForm()

        if form.validate_on_submit():
            # Create new user
            user = models.User()
            user.username = request.form["username"]
            password = request.form["password"]

            # Salt and hash password
            sh_password = werkzeug.security.generate_password_hash(
                password,
                method="pbkdf2:sha256",
                salt_length=8
            )

            user.password = sh_password

            # Check if username already exists in database
            username_search = db.session.execute(select(models.User).filter_by(username=user.username)).first()
            if username_search:
                # Debug message
                print("Username already in use. Please choose a new username.")
                flash("Username already in use. Please choose a new username.")
                return redirect(url_for("register"))
            else:
                # Add user to database
                db.session.add(user)
                db.session.commit()
                # Login user
                # Debug message
                print(f"Registration successful {user.username}")
                login_user(user)
                return redirect(url_for("home"))

        return render_template("register.html", form=form)

    # Existing user login
    @flask_app.route("/login", methods=["GET", "POST"])
    def login():

        # Check if user is already logged in and redirect if they are
        if current_user.is_authenticated:
            # Debug message
            print("User already logged in.")
            return redirect(url_for("home"))

        form = forms.LoginForm()

        if form.validate_on_submit():

            username = request.form["username"]
            password = request.form["password"]
            user = db.session.execute(select(models.User).filter_by(username=username)).scalar()

            if user:
                if werkzeug.security.check_password_hash(pwhash=user.password, password=password):
                    # Login user
                    # Debug message
                    print(f"Login successful {user.username}")
                    login_user(user)
                    return redirect(url_for("home"))
                else:
                    # Debug message
                    print("Incorrect password or username.")
                    flash("Incorrect password or username.")
                    return redirect(url_for("login"))
            else:
                # Debug message
                print("Username not found. Please check login details.")
                flash("Username not found. Please check login details.")
                return redirect(url_for("login"))

        return render_template("login.html", form=form)

    # Logout user
    @flask_app.route("/logout")
    @login_required
    def logout():
        logout_user()
        print("Logged out")
        return redirect(url_for("home"))

    @flask_app.route("/<username>/delete")
    @login_required
    def delete_user():
        return redirect(url_for("home"))

    @flask_app.route("/<username>/edit")
    @login_required
    def edit_user():
        return render_template("user_settings.html")

    #   =======================================
    #                  Campaign
    #   =======================================

    # View campaign overview
    @flask_app.route("/<campaign_name>")
    def show_timeline(campaign_name):

        # Get the target campaign's id from the url argument. Campaign ids are stored as an integer in the database.
        target_id = int(request.args["id"])

        campaign = db.session.execute(select(models.Campaign).filter_by(id=target_id)).scalar()

        return render_template("timeline.html", campaign=campaign)

    # Create new campaign
    @flask_app.route("/create_campaign", methods=["GET", "POST"])
    @login_required
    def create_campaign():

        form = forms.CreateCampaignForm()

        if form.validate_on_submit():
            user = current_user

            new_campaign = models.Campaign()

            new_campaign.title = request.form["title"]
            new_campaign.description = request.form["description"]

            # Add new campaign to database
            db.session.add(new_campaign)
            # Add current user as campaign member
            user.campaigns.append(new_campaign)
            # Give current user campaign editing permissions
            user.permissions.append(new_campaign)

            db.session.commit()

            campaign = db.session.execute(select(models.Campaign).filter_by(id=new_campaign.id)).scalar()

            return redirect(url_for("show_timeline", campaign_name=campaign.title, id=campaign.id))

        return render_template("new_campaign.html", form=form)

    # Edit campaign data
    @flask_app.route("/edit_campaign/<campaign_name>")
    def edit_campaign(campaign_name):
        return render_template("edit_campaign.html")

    # Edit campaign users
    @flask_app.route("/edit_campaign/<campaign_name>/add_users")
    def add_campaign_users(campaign_name):
        return render_template("edit_campaign.html")

    #   =======================================
    #                  Event
    #   =======================================

    # View event
    @flask_app.route("/<campaign_name>/<event_name>")
    def view_event(campaign_name, event_name):
        return render_template("event.html")

    # Add new event
    @flask_app.route("/<campaign_name>/new_event", methods=["GET", "POST"])
    @login_required
    def add_event(campaign_name):

        # Get the target campaign's id from the url argument. Campaign ids are stored as an integer in the database.
        target_id = int(request.args["id"])

        # Check if the user has permissions to edit the target campaign.
        for editable_campaign in current_user.permissions:
            if target_id == editable_campaign.id:
                # Select the campaign to be edited
                campaign_query = db.session.execute(select(models.Campaign).filter_by(title=campaign_name,
                                                                                      id=target_id)).scalar()

                form = forms.CreateEventForm()

                # Check if user has submitted a new event
                if form.validate_on_submit():
                    title = request.form["title"]
                    # event_type to avoid shadowing built-in name 'type'
                    event_type = request.form["type"]
                    date = request.form["date"]
                    # Convert date to datetime object
                    date_format = '%Y-%m-%d %H:%M:%S'
                    date_obj = datetime.strptime(date, date_format)

                    location = request.form["location"]
                    belligerents = request.form["belligerents"]
                    body = request.form["body"]
                    result = request.form["result"]

                    # Create new event object using form data
                    event = models.Event()
                    event.title = title
                    event.type = event_type
                    event.date = date_obj
                    event.location = location
                    event.belligerents = belligerents
                    event.body = body
                    event.result = result

                    event.parent_campaign = campaign_query

                    # Add event to database
                    db.session.add(event)
                    db.session.commit()

                    return redirect(url_for("show_timeline", id=target_id))

                return render_template("new_event.html", form=form)

            else:
                # Redirect to homepage if the user is somehow trying to edit a campaign that they
                # do not have permission for.
                return redirect(url_for("home"))

    # Edit existing event
    @flask_app.route("/<campaign_name>/<event_name>/edit", methods=["GET", "POST"])
    @login_required
    def edit_event(campaign_name, event_name):

        # Get the target event's id from the url argument.
        target_id = int(request.args["id"])
        event = db.session.execute(select(models.Event).filter_by(title=event_name, id=target_id)).scalar()

        # Check if the user has permissions to edit the event.
        for editable_campaign in current_user.permissions:
            if event.id == editable_campaign.id:

                form = forms.CreateEventForm(obj=event)

                if form.validate_on_submit():
                    # Update event data
                    title = request.form["title"]
                    # event_type to avoid shadowing built-in name 'type'
                    event_type = request.form["type"]
                    date = request.form["date"]
                    # Convert date to datetime object
                    date_format = '%Y-%m-%d %H:%M:%S'
                    date_obj = datetime.strptime(date, date_format)

                    location = request.form["location"]
                    belligerents = request.form["belligerents"]
                    body = request.form["body"]
                    result = request.form["result"]

                    # Update event attributes
                    event.title = title
                    event.type = event_type
                    event.date = date_obj
                    event.location = location
                    event.belligerents = belligerents
                    event.body = body
                    event.result = result

                    # Update the database
                    db.session.add(event)
                    db.session.commit()

                    return redirect(url_for("view_event",
                                            campaign_name=campaign_name,
                                            event_name=title))

                return render_template("edit_event.html",
                                       campaign_name=campaign_name,
                                       event_name=event_name,
                                       id=target_id)

        # Redirect to homepage if the user is somehow trying to edit an event that they
        # do not have permission for.
        return redirect(url_for("home"))

    # Delete existing event
    @flask_app.route("/<campaign_name>/<event_name>/delete")
    def delete_event(campaign_name, event_name):
        return redirect(url_for("show_timeline"))

    #   =======================================
    #            User Data Management
    #   =======================================

    # Backup campaign data
    @flask_app.route("/<campaign_name>/backup")
    def campaign_backup(campaign_name):

        target_id = int(request.args["id"])
        # Export campaign data as json file.
        return redirect(url_for("show_timeline", id=target_id))

    # Import campaign backup
    @flask_app.route("/<campaign_name>/import")
    def import_campaign(campaign_name):

        target_id = int(request.args["id"])
        # Export campaign data as json file.
        return redirect(url_for("show_timeline", id=target_id))

    # Export campaign timeline as pdf
    @flask_app.route("/<campaign_name>/export")
    def export_campaign(campaign_name):

        target_id = int(request.args["id"])
        # Export campaign data as json file.
        return redirect(url_for("show_timeline", id=target_id))
