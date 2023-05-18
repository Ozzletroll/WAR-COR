from flask import render_template, redirect, request, url_for, flash
from sqlalchemy import select
from flask_login import login_user, login_required, current_user, logout_user
import werkzeug
from werkzeug.security import generate_password_hash, check_password_hash

import forms
import models

from app import db


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
        return render_template("timeline.html")

    # Create new campaign
    @flask_app.route("/create_campaign")
    def create_campaign():
        return render_template("new_campaign.html")

    # Edit campaign data
    @flask_app.route("/edit_campaign/<campaign_name>")
    def edit_campaign(campaign_name):
        return render_template("edit_campaign.html")

    # Edit campaign users
    @flask_app.route("/edit_campaign/<campaign_name>/add_users")
    def add_campaign_users(campaign_name):

        user_to_add = "USERNAME OF USER TO BE ADDED TO CAMPAIGN"

        user = db.session.execute(select(models.User).filter_by(username=user_to_add)).scalar()
        campaign = db.session.execute(select(models.Campaign).filter_by(title=campaign_name)).scalar()

        # Add user to campaign:
        user.campaigns.append(campaign)
        db.session.commit()

        # Give user campaign permissions:
        user.permissions.append(campaign)

        # Remove user from campaign:
        # user.campaigns.remove(campaign)
        # db.session.commit()
        # Can be iterated through:
        # for campaign in user.campaigns:
        #     print(campaign.title)
        #
        # See https://www.youtube.com/watch?v=47i-jzrrIGQ for a reminder.

        return render_template("edit_campaign.html")

    #   =======================================
    #                  Event
    #   =======================================

    # View event
    @flask_app.route("/<campaign_name>/<event_name>")
    def view_event(campaign_name, event_name):
        return render_template("event.html")

    # Add new event
    @flask_app.route("/<campaign_name>/new_event")
    def add_event(campaign_name):
        return render_template("new_event.html")

    # Edit existing event
    @flask_app.route("/<campaign_name>/<event_name>/edit")
    def edit_event(campaign_name, event_name):
        return render_template("edit_event.html")

    # Delete existing event
    @flask_app.route("/<campaign_name>/<event_name>/delete")
    def delete_event(campaign_name, event_name):
        return redirect(url_for("show_timeline"))
