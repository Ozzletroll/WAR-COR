from flask import render_template, redirect, request, url_for, flash
from sqlalchemy import select
from flask_login import login_user, login_required, current_user, logout_user
import werkzeug
from werkzeug.security import generate_password_hash

import forms
import models

from app import db
from routes.user import bp

#   =======================================
#                  User
#   =======================================


# New user registration
@bp.route("/register", methods=["GET", "POST"])
def register():

    # Check if user is already logged in and redirect if they are
    if current_user.is_authenticated:
        # Debug message
        print("User already logged in.")
        return redirect(url_for("home.home"))

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
            return redirect(url_for("user.register"))
        else:
            # Add user to database
            db.session.add(user)
            db.session.commit()
            # Login user
            # Debug message
            print(f"Registration successful {user.username}")
            login_user(user)
            return redirect(url_for("campaign.campaigns"))

    return render_template("register.html", form=form)


# Existing user login
@bp.route("/login", methods=["GET", "POST"])
def login():

    # Check if user is already logged in and redirect if they are
    if current_user.is_authenticated:
        # Debug message
        print("User already logged in.")
        return redirect(url_for("home.home"))

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
                return redirect(url_for("campaign.campaigns"))
            else:
                # Debug message
                print("Incorrect password or username.")
                flash("Incorrect password or username.")
                return redirect(url_for("user.login"))
        else:
            # Debug message
            print("Username not found. Please check login details.")
            flash("Username not found. Please check login details.")
            return redirect(url_for("user.login"))

    return render_template("login.html", form=form)


# Logout user
@bp.route("/logout")
@login_required
def logout():
    logout_user()
    print("Logged out")
    return redirect(url_for("home.home"))


# Access user page
@bp.route("/user/<username>")
@login_required
def user_page(username):

    user = db.session.execute(select(models.User).filter_by(username=username)).scalar()

    if user.id == current_user.id:
        return render_template("user_page.html", user=user)

    return redirect(url_for("home.home"))


@bp.route("/user/<username>/delete", methods=["GET", "POST"])
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
                    return redirect(url_for("home.home"))
                else:
                    # Debug message
                    print("Incorrect password or username.")
                    flash("Incorrect password or username.")
                    return redirect(url_for("user.delete_user", username=current_user.username))
            else:
                # Debug message
                print("Username not found. Please check username and password.")
                flash("Username not found. Please check username and password.")
                return redirect(url_for("user.user_settings", username=current_user.username))
        else:
            return render_template("delete_user.html", form=form)

    # Redirect if a user is trying to access another user's delete route
    else:
        return redirect(url_for("home.home"))


@bp.route("/user/<username>/edit")
@login_required
def edit_user():
    return render_template("user_settings.html")
