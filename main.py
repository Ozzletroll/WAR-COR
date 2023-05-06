from flask import Flask, render_template, redirect, request, url_for, flash, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
from flask_login import UserMixin, login_user, login_required, current_user, logout_user
import werkzeug
from werkzeug.security import generate_password_hash, check_password_hash

import forms
import models
from app import create_app
from app import db

# Initial setup:
# TODO: Create and style page templates
#     TODO: Create index.html
#     TODO: Create register.html
#     TODO: Create login.html
#     TODO: Create user_settings.html
#     TODO: Create timeline.html
#     TODO: Create new_campaign.html
#     TODO: Create edit_campaign.html
#     TODO: Create event.html
#     TODO: Create new_event.html
#     TODO: Create edit_event.html

# TODO: Implement basic page navigation
# TODO: Implement user login/logout functionality
# TODO: Define User database models
# TODO: Define Campaign database models
# TODO: Define Event database models
# TODO: Define Comment database models

# TODO: Main functionality
#   TODO: Add campaign creation
#   TODO: Add campaign viewing
#   TODO: Add campaign editing
#   TODO: Add campaign deletion
#   TODO: Add campaign user invitation

#   TODO: Add event creation
#   TODO: Add event viewing
#   TODO: Add event editing
#   TODO: Add event deletion
#   TODO: Add event commenting

flask_app = create_app()


# User loader callback
# https://flask-login.readthedocs.io/en/latest/#login-example
@flask_app.login_manager.user_loader
def load_user(user_id):
    # TODO: Update database query to new syntax
    return db.session.query(models.User).get(user_id)


#   =======================================
#                  HOMEPAGE
#   =======================================


# Basic navigation
@flask_app.route("/")
def home():
    return render_template("index.html")


#   =======================================
#                  User
#   =======================================


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


@flask_app.route("/login", methods=["GET", "POST"])
def login():

    form = forms.LoginForm()

    if form.validate_on_submit():

        username = request.form["username"]
        password = request.form["password"]
        user = db.session.execute(select(models.User).filter_by(username=username)).first()

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
            flash("Username not found. Please check login details.")
            return redirect(url_for("login"))

    return render_template("login.html", form=form)


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


if __name__ == "__main__":
    flask_app.run(debug=True)

