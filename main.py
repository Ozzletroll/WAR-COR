from flask import Flask, render_template, redirect, request, url_for, flash, abort
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from database import create_database

# TODO: Move database models to database.py

# TODO: Create and style page templates
# TODO: Implement basic page navigation
# TODO: Add new user registration
# TODO: Implement user login/logout functionality
# TODO: Define User database models
# TODO: Define Campaign database models
# TODO: Define Event database models
# TODO: Define Comment database models

flask_app = create_app()
db = create_database()

#   =======================================
#                  ROUTES
#   =======================================


# Basic navigation
@flask_app.route("/")
def home():
    return render_template("index.html")


# User management
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
    return render_template(edit_user.html)


# Campaign creation/editing/viewing
@flask_app.route("/create_campaign")
def create_campaign():
    return render_template("create.html")


@flask_app.route("/edit_campaign/<campaign_name>")
def edit_campaign():
    return render_template("create.html")


@flask_app.route("/<campaign_name>")
def show_timeline():
    return render_template("timeline.html")


@flask_app.route("/<campaign_name>/add_event")
def add_event():
    return render_template("event.html")


@flask_app.route("/<campaign_name>/edit_event")
def edit_event():
    return render_template("event.html")


@flask_app.route("/<campaign_name>/delete_event")
def delete_event():
    return render_template("event.html")


if __name__ == "__main__":
    flask_app.run(debug=True)

