from flask import render_template, redirect, request, url_for, flash, session
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

        # Check if user is already logged in and redirect if they are
        if current_user.is_authenticated:
            # Debug message
            print("User already logged in.")
            return redirect(url_for("home"))

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

    # Access user page
    @flask_app.route("/user/<username>")
    @login_required
    def user_page(username):

        user = db.session.execute(select(models.User).filter_by(username=username)).scalar()

        if user.id == current_user.id:
            return render_template("user_page.html", user=user)

        return redirect(url_for("home"))

    @flask_app.route("/user/<username>/delete", methods=["GET", "POST"])
    @login_required
    def delete_user(username):

        if current_user.username == username:

            form = forms.LoginForm()

            if form.validate_on_submit():

                user_id = current_user.id

                search_username = request.form["username"]
                password = request.form["password"]
                user = db.session.execute(select(models.User).filter_by(id=user_id, username=search_username)).scalar()

                if user:
                    if werkzeug.security.check_password_hash(pwhash=user.password, password=password):
                        # Delete user from database
                        db.session.delete(user)
                        db.session.commit()
                        # Debug message
                        print(f"{user.username} account deleted.")
                        flash(f"{user.username} account deleted.")
                        return redirect(url_for("home"))
                    else:
                        # Debug message
                        print("Incorrect password or username.")
                        flash("Incorrect password or username.")
                        return redirect(url_for("delete_user", username=current_user.username))
                else:
                    # Debug message
                    print("Username not found. Please check username and password.")
                    flash("Username not found. Please check username and password.")
                    return redirect(url_for("user_settings", username=current_user.username))
            else:
                return render_template("delete_user.html", form=form)

        # Redirect if a user is trying to access another user's delete route
        else:
            return redirect(url_for("home"))

    @flask_app.route("/user/<username>/edit")
    @login_required
    def edit_user():
        return render_template("user_settings.html")

    #   =======================================
    #                  Campaign
    #   =======================================

    # View all users campaigns
    @flask_app.route("/campaigns")
    def campaigns():
        return render_template("campaigns.html")

    # View campaign overview
    @flask_app.route("/campaigns/<campaign_name>")
    def show_timeline(campaign_name):

        target_id = session.get("campaign_id", None)
        campaign = db.session.execute(select(models.Campaign).filter_by(id=target_id)).scalar()

        return render_template("timeline.html", campaign=campaign)

    # Create new campaign
    @flask_app.route("/campaigns/create_campaign", methods=["GET", "POST"])
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
            session["campaign_id"] = campaign.id
            return redirect(url_for("show_timeline", campaign_name=campaign.title))

        return render_template("new_campaign.html", form=form)

    # Edit campaign data
    @flask_app.route("/campaigns/<campaign_name>/edit", methods=["GET", "POST"])
    def edit_campaign(campaign_name):

        target_campaign_id = session.get("campaign_id", None)

        campaign = db.session.execute(select(models.Campaign).filter_by(id=target_campaign_id)).scalar()

        # Check if the user has permissions to edit the target campaign.
        if campaign in current_user.permissions:

            form = forms.CreateCampaignForm(obj=campaign)

            if form.validate_on_submit():

                campaign.title = request.form["title"]
                campaign.description = request.form["description"]

                db.session.add(campaign)
                db.session.commit()

                session["campaign_id"] = campaign.id
                return redirect(url_for("show_timeline", campaign_name=campaign.title))

            return render_template("edit_campaign.html", form=form)

        # Redirect to homepage if user is trying to access a campaign they don't have permissions for.
        return redirect(url_for("home"))

    # Edit campaign users
    @flask_app.route("/campaigns/<campaign_name>/add_users", methods=["GET", "POST"])
    @login_required
    def add_campaign_users(campaign_name):

        target_campaign_id = session.get("campaign_id", None)

        campaign = db.session.execute(select(models.Campaign).filter_by(id=target_campaign_id)).scalar()

        # Check if the user has permissions to edit the target campaign.
        if campaign in current_user.permissions:

            form = forms.AddUserForm()

            if form.validate_on_submit():

                user_to_add = request.form["username"]

                # Check if username exists
                user = db.session.execute(select(models.User).filter_by(username=user_to_add)).scalar()
                if user:
                    # Get campaign and add user as member
                    user.campaigns.append(campaign)
                    db.session.commit()
                else:
                    print("User not in database, please check username.")
                    flash("User not in database, please check username.")
                return redirect(url_for("edit_campaign", campaign_name=campaign_name))

            return render_template("edit_campaign.html", form=form)

        # Redirect to homepage if user is trying to access a campaign they don't have permissions for.
        return redirect(url_for("home"))

    # Remove campaign users
    @flask_app.route("/campaigns/<campaign_name>/remove_users/<username>", methods=["GET"])
    @login_required
    def remove_campaign_users(campaign_name, username):

        target_campaign_id = session.get("campaign_id", None)
        campaign = db.session.execute(select(models.Campaign).filter_by(id=target_campaign_id)).scalar()

        # Check if the user has permissions to edit the target campaign.
        if campaign in current_user.permissions:

            user_to_remove = username

            # Check if username exists
            user = db.session.execute(select(models.User).filter_by(username=user_to_remove)).scalar()
            if user:
                # Check is user is actually a member of the campaign
                if user in campaign.members:
                    user.campaigns.remove(campaign)
                    flash(f"Removed user {user} from campaign.")
                    print(f"Removed user {user} from campaign.")
                # Remove editing permissions if they exist
                if campaign in user.permissions:
                    user.permissions.remove(campaign)
                    flash(f"Removed user {user}'s campaign permissions.")
                    print(f"Removed user {user}'s campaign permissions.")
                db.session.commit()
            else:
                print("User not in database, please check username.")
                flash("User not in database, please check username.")
            return redirect(url_for("edit_campaign", campaign_name=campaign_name))

        # Redirect to homepage if user is trying to access a campaign they don't have permissions for.
        return redirect(url_for("home"))

    #   =======================================
    #                  Event
    #   =======================================

    # View event
    @flask_app.route("/campaigns/<campaign_name>/<event_name>")
    def view_event(campaign_name, event_name):

        target_event_id = session.get("event_id", None)
        event = db.session.execute(select(models.Event).filter_by(id=target_event_id)).scalar()

        return render_template("event.html", event=event)

    # Add new event
    @flask_app.route("/campaigns/<campaign_name>/new_event", methods=["GET", "POST"])
    @login_required
    def add_event(campaign_name):

        target_campaign_id = session.get("campaign_id", None)

        campaign = db.session.execute(select(models.Campaign).filter_by(id=target_campaign_id)).scalar()

        # Check if the user has permissions to edit the target campaign.
        if campaign in current_user.permissions:

            form = forms.CreateEventForm()

            # Check if user has submitted a new event
            if form.validate_on_submit():
                # Create new event object using form data
                event = models.Event()
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

                event.parent_campaign = campaign

                # Add event to database
                db.session.add(event)
                db.session.commit()

                session["campaign_id"] = campaign.id

                return redirect(url_for("show_timeline",
                                        campaign_name=campaign.title))

            return render_template("new_event.html", form=form)

        else:
            # Redirect to homepage if the user is somehow trying to edit a campaign that they
            # do not have permission for.
            return redirect(url_for("home"))

    # Edit existing event
    @flask_app.route("/campaigns/<campaign_name>/<event_name>/edit", methods=["GET", "POST"])
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

                return redirect(url_for("view_event",
                                        campaign_name=campaign_name,
                                        event_name=event.title))

            return render_template("edit_event.html",
                                   campaign_name=campaign_name,
                                   event_name=event_name)

        # Redirect to homepage if the user is somehow trying to edit an event that they
        # do not have permission for.
        return redirect(url_for("home"))

    # Delete existing event
    @flask_app.route("/campaigns/<campaign_name>/<event_name>/delete", methods=["GET"])
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

        return redirect(url_for("show_timeline", campaign_name=campaign_name))

    #   =======================================
    #            User Data Management
    #   =======================================

    # Backup campaign data
    @flask_app.route("/campaigns/<campaign_name>/backup")
    def campaign_backup(campaign_name):

        target_campaign_id = session.get("campaign_id", None)
        # Export campaign data as json file.
        return redirect(url_for("show_timeline", id=target_campaign_id))

    # Import campaign backup
    @flask_app.route("/campaigns/<campaign_name>/import")
    def import_campaign(campaign_name):

        target_campaign_id = session.get("campaign_id", None)
        # Export campaign data as json file.
        return redirect(url_for("show_timeline", id=target_campaign_id))

    # Export campaign timeline as pdf
    @flask_app.route("/campaigns/<campaign_name>/export")
    def export_campaign(campaign_name):

        target_campaign_id = session.get("campaign_id", None)
        # Export campaign data as json file.
        return redirect(url_for("show_timeline", id=target_campaign_id))
