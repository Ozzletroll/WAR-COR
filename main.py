import flask
from flask import Flask, render_template, redirect, request, url_for, flash, abort
import os
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")


# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///war_cor.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Basic navigation routes
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/logout")
def logout():
    return redirect(url_for("home"))


# Campaign creation/editing/viewing routes
@app.route("/create_campaign")
def create_campaign():
    return render_template("create.html")


@app.route("/edit_campaign/<campaign_name>")
def edit_campaign():
    return render_template("create.html")


@app.route("/<campaign_name>")
def show_timeline():
    return render_template("timeline.html")


@app.route("/<campaign_name>/add_event")
def add_event():
    return render_template("event.html")


@app.route("/<campaign_name>/edit_event")
def edit_event():
    return render_template("event.html")


@app.route("/<campaign_name>/delete_event")
def delete_event():
    return render_template("event.html")


if __name__ == "__main__":
    app.run(debug=True)

