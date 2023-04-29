import flask
from flask import Flask, render_template, redirect, request, url_for, flash, abort
import os
from flask_sqlalchemy import SQLAlchemy

# TODO: Create and style page templates
# TODO: Implement basic page navigation
# TODO: Add new user registration
# TODO: Implement user login/logout functionality
# TODO: Define User database models
# TODO: Define Campaign database models
# TODO: Define Event database models
# TODO: Define Comment database models


# Configure Flask app
def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///war_cor.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    return app


flask_app = create_app()


# Configure database
db = SQLAlchemy(flask_app)


# Define database models
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    # Basic user data
    username = db.Column(db.String(30))
    email = db.Column(db.String(250))
    password = db.Column(db.String(250))

    # Database relationships

    # campaigns =
    # comments =


class Campaign(db.Model):
    __tablename__ = "campaigns"

    id = db.Column(db.Integer, primary_key=True)

    # Basic campaign data
    title = db.Column(db.String(250))

    # Database relationships

    # participants =
    # events =
    # comments =


class Event(db.Model):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)


class Comments(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)


# Initialise database
with flask_app.app_context():
    db.create_all()


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

