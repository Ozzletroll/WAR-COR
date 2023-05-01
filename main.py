from flask import Flask, render_template, redirect, request, url_for, flash, abort
from flask_sqlalchemy import SQLAlchemy
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
# TODO: Add new user registration
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
        user.password = request.form["password"]

        # Check if username already exists in database
        # TODO: Add username database query
        username_search = False
        if username_search:
            flash("Username already taken. Please choose a new username.")
            return redirect(url_for("register"))
        else:
            # Add user to database
            db.session.add(user)
            db.session.commit()
            # Login user
            # TODO: Add user login
            return redirect(url_for("home"))

    return render_template("register.html", form=form)


@flask_app.route("/login")
def login():

    form = forms.LoginForm()

    if form.validate_on_submit():

        username = request.form["username"]
        password = request.form["password"]

        # TODO: Check username exists in database
        user = "DATABASE QUERY GOES HERE"

        if user:
            # TODO: Check if password matches database
            if werkzeug.security.check_password_hash(pwhash=user.password, password=password):
                # Login user
                return redirect(url_for("home"))
            else:
                flash("Incorrect password or username.")
                return redirect(url_for("login"))

    return render_template("login.html", form=form)


@flask_app.route("/logout")
def logout():
    return redirect(url_for("home"))


@flask_app.route("/<username>/delete")
def delete_user():
    return redirect(url_for("home"))


@flask_app.route("/<username>/edit")
def edit_user():
    return render_template("user_settings.html")

#   =======================================
#                  Campaign
#   =======================================


# View campaign overview
@flask_app.route("/<campaign_name>")
def show_timeline():
    return render_template("timeline.html")


# Create new campaign
@flask_app.route("/create_campaign")
def create_campaign():
    return render_template("new_campaign.html")


# Edit campaign data
@flask_app.route("/edit_campaign/<campaign_name>")
def edit_campaign():
    return render_template("edit_campaign.html")


#   =======================================
#                  Event
#   =======================================

# View event
@flask_app.route("/<campaign_name>/<event_name>")
def view_event():
    return render_template("event.html")


# Add new event
@flask_app.route("/<campaign_name>/new_event")
def add_event():
    return render_template("new_event.html")


# Edit existing event
@flask_app.route("/<campaign_name>/<event_name>/edit")
def edit_event():
    return render_template("edit_event.html")


# Delete existing event
@flask_app.route("/<campaign_name>/<event_name>/delete")
def delete_event():
    return redirect(url_for("show_timeline"))


if __name__ == "__main__":
    flask_app.run(debug=True)

