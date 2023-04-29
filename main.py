from flask import Flask, render_template, redirect, request, url_for, flash, abort
from flask_sqlalchemy import SQLAlchemy

from app import create_app

# TODO: Create and style page templates
# TODO: Implement basic page navigation
# TODO: Add new user registration
# TODO: Implement user login/logout functionality
# TODO: Define User database models
# TODO: Define Campaign database models
# TODO: Define Event database models
# TODO: Define Comment database models

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


@flask_app.route("/register")
def register():
    return render_template("register.html")


@flask_app.route("/login")
def login():
    return render_template("login.html")


@flask_app.route("/logout")
def logout():
    return redirect(url_for("home"))


@flask_app.route("/<username>/delete")
def delete_user():
    return redirect(url_for("home"))


@flask_app.route("/<username>/edit")
def edit_user():
    return render_template("edit_user.html")

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

