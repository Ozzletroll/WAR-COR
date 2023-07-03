from flask import render_template, redirect, request, url_for, flash
from sqlalchemy import select
from flask_login import login_user, login_required, current_user, logout_user
import werkzeug
from werkzeug.security import generate_password_hash

import auth
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
    return redirect(url_for("home.home"))


# Access user page
@bp.route("/user/<username>", methods=["GET", "POST"])
@login_required
def user_page(username) :

    user = db.session.execute(select(models.User).filter_by(username=username)).scalar()

    # Check if the user is actually the owner of the account they are trying to modify
    auth.user_verification(user)

    callsign_form = forms.ChangeCallsignForm()
    username_form = forms.ChangeUsernameForm()
    password_form = forms.ChangePasswordForm()

    return render_template("user_page.html", 
                            user=user, 
                            callsign_form=callsign_form,
                            username_form=username_form,
                            password_form=password_form)


@bp.route("/user/<username>/update_callsign", methods=["GET", "POST"])
@login_required
def update_callsign(username):

    callsign_form = forms.ChangeCallsignForm()

    if callsign_form.validate_on_submit():

        user_id = request.args["user_id"]
        campaign_id = request.args["campaign_id"]
        callsign = request.form["callsign"]
        
        # Update the users callsign
        user_campaign = db.session.execute(select(models.UserCampaign).filter_by(user_id=user_id, campaign_id=campaign_id)).scalar()
        user_campaign.callsign = callsign

        db.session.commit()

        flash("Callsign updated")

    else:
        # Flash any form errors  
        for field_name, errors in callsign_form.errors.items():
            for error_message in errors:
                flash(field_name + ": " + error_message)

    # Redirect back to user page
    return redirect(url_for("user.user_page", username=username))   


@bp.route("/user/<username>/change_username", methods=["GET", "POST"])
@login_required
def change_username(username):

    user = db.session.execute(select(models.User).filter_by(username=username)).scalar()
    auth.user_verification(user)
    username_form = forms.ChangeUsernameForm()

    if username_form.validate_on_submit():
        
        new_username = request.form["new_username"]

        # Check if new username is not already in use
        username_check = db.session.execute(select(models.User).filter_by(username=new_username)).scalar()
        if not username_check:

            # Set username to new value
            user.username = new_username
            db.session.commit()
            flash("Username updated")
        
        # Otherwise, redirect back to user page
        else:
            flash("Username already in use, please choose another")

    else:
        # Flash any form errors
        for field_name, errors in username_form.errors.items():
            for error_message in errors:
                flash(error_message)      

    return redirect(url_for("user.user_page", username=user.username))
        

@bp.route("/user/<username>/change_password", methods=["GET", "POST"])
@login_required
def change_password(username):

    user = db.session.execute(select(models.User).filter_by(username=username)).scalar()
    auth.user_verification(user)

    # Check if the user matching given parameters exists in database
    if user:

        password_form = forms.ChangePasswordForm()

        # Password change form is submitted
        if password_form.validate_on_submit():
            
            old_password = request.form["old_password"]
            new_password = request.form["new_password"]

            # Check if the given old password matches the db password
            if werkzeug.security.check_password_hash(pwhash=user.password, password=old_password):
                
                # Salt and hash new password
                sh_password = werkzeug.security.generate_password_hash(
                    new_password,
                    method="pbkdf2:sha256",
                    salt_length=8
                )

                user.password = sh_password

                # Update database
                db.session.commit()

                flash("Password updated")
                return redirect(url_for("user.user_page", username=user.username))
            
            else:
                flash("Incorrect password")
                return redirect(url_for("user.user_page", username=user.username))

        else:
            # Flash any form errors
            for field_name, errors in password_form.errors.items():
                for error_message in errors:
                    flash(error_message)        

    # Redirect to user page
    return redirect(url_for("user.user_page", username=user.username))


@bp.route("/user/<username>/delete", methods=["GET", "POST"])
@login_required
def delete_user(username):

    user = db.session.execute(select(models.User).filter_by(username=username)).scalar()
    auth.user_verification(user)

    # Create login form to check credentials
    form = forms.LoginForm()

    if form.validate_on_submit():

        search_username = request.form["username"]
        password = request.form["password"]

        search_user = db.session.execute(select(models.User).filter_by(username=search_username)).scalar()

        if search_user:
            if werkzeug.security.check_password_hash(pwhash=user.password, password=password):
                
                # Check if user deletion will leave any campaigns without any members
                for campaign in user.campaigns:
                    if len(campaign.members) == 1:
                        db.session.delete(campaign)
                
                # Delete user from database
                logout_user()
                db.session.delete(user)
                
                # Commit changes
                db.session.commit()
                return redirect(url_for("home.home"))
            else:
                flash("Authentication failed. Incorrect password.")
                return redirect(url_for("user.user_page", username=current_user.username))
        else:
            flash("Authentication failed. Incorrect username.")
            return redirect(url_for("user.user_page", username=current_user.username))
    else:
        # Change LoginForm submit button text
        form.submit.label.text = "Terminate Contract"

        return render_template("delete_user.html", form=form)


