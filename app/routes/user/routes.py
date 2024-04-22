from flask import render_template, redirect, request, url_for, flash, session
from sqlalchemy import select
from flask_login import login_user, login_required, current_user, logout_user

from app.forms import forms
from app import db, models, limiter
from app.utils import authenticators, messengers

from app.routes.user import bp


#   =======================================
#                  User
#   =======================================

# New user registration
@bp.route("/register", methods=["GET", "POST"])
def register():

    # Check if user is already logged in and redirect if they are
    if current_user.is_authenticated:
        return redirect(url_for("home.home"))

    form = forms.RegisterUserForm()

    if form.validate_on_submit():

        proposed_username = request.form["username"]
        proposed_email = request.form["email"]
        # Check if username already exists in database
        username_search = (db.session.execute(select(models.User)
                           .filter_by(username=proposed_username))
                           .first())
        email_search = (db.session.execute(select(models.User)
                        .filter_by(email=proposed_email))
                        .first())

        if username_search:
            flash("Username already in use, please choose a different username")
            return redirect(url_for("user.register"))
        elif email_search:
            flash("Account already registered with that email, please login instead")
            return redirect(url_for("user.register"))
        else:
            # Create new user
            user = models.User()
            user.update(form=request.form,
                        new=True)
            # Login user
            login_user(user)
            return redirect(url_for("campaign.campaigns"))

    return render_template("pages/register.html", form=form)


# Existing user login
@bp.route("/login", methods=["GET", "POST"])
def login():

    # Check if user is already logged in and redirect if they are
    if current_user.is_authenticated:
        return redirect(url_for("home.home"))

    form = forms.LoginForm()

    if form.validate_on_submit():

        username = request.form["username"]
        password = request.form["password"]

        user = (db.session.execute(select(models.User)
                .filter_by(username=username)).scalar())

        if user:
            if user.check_password(password):
                login_user(user)
                return redirect(request.args.get("next") or url_for("campaign.campaigns"))
            else:
                flash("Incorrect password or username")
                return redirect(url_for("user.login"))
        else:
            flash("Incorrect password or username")
            return redirect(url_for("user.login"))

    return render_template("pages/login.html", form=form)


# Logout user
@bp.route("/logout")
@login_required
def logout():

    logout_user()
    session.clear()

    return redirect(url_for("home.home"))


# Access user page
@bp.route("/user/<username>", methods=["GET"])
@login_required
def user_page(username):

    user = (db.session.query(models.User)
            .filter(models.User.username == username)
            .first_or_404(description="No matching user found"))

    # Check if the user is actually the owner of the account they are trying to modify
    authenticators.user_verification(user)

    remove_form = forms.AddUserForm()
    callsign_form = forms.ChangeCallsignForm()
    username_form = forms.ChangeUsernameForm()
    password_form = forms.ChangePasswordForm()

    # Set url for back button
    if request.referrer and "/user" not in request.referrer:
        session["previous_url"] = request.referrer

    return render_template("pages/user_page.html",
                           user=user,
                           remove_form = remove_form,
                           callsign_form=callsign_form,
                           username_form=username_form,
                           password_form=password_form)


@bp.route("/user/<username>/update-callsign", methods=["POST"])
@login_required
def update_callsign(username):

    callsign_form = forms.ChangeCallsignForm()

    if callsign_form.validate_on_submit():

        user_id = request.args["user_id"]
        campaign_id = request.args["campaign_id"]
        callsign = request.form["callsign"]
        
        # Update the users callsign
        user_campaign = (db.session.execute(select(models.UserCampaign)
                         .filter_by(user_id=user_id, campaign_id=campaign_id))
                         .scalar())
        
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


@bp.route("/user/<username>/change-username", methods=["POST"])
@login_required
def change_username(username):

    user = (db.session.query(models.User)
            .filter(models.User.username == username)
            .first_or_404(description="No matching user found"))
    
    authenticators.user_verification(user)

    # Check if new username is not already in use
    new_username = request.form["username"]

    if len(new_username) < 3:
        flash("New username must be 3 or more characters")
        return redirect(url_for("user.user_page", username=user.username))

    username_check = (db.session.execute(select(models.User)
                      .filter_by(username=new_username))
                      .scalar())
    
    if not username_check:
        # Set username to new value
        user.update(form=request.form)
        flash("Username updated")
    
    # Otherwise, redirect back to user page
    else:
        flash("Username already in use, please choose another")

    return redirect(url_for("user.user_page", username=user.username))
        

@bp.route("/user/<username>/change-password", methods=["POST"])
@login_required
def change_password(username):

    user = (db.session.query(models.User)
            .filter(models.User.username == username)
            .first_or_404(description="No matching user found"))
    
    authenticators.user_verification(user)

    # Check if the user matching given parameters exists in database
    if user:
        password_form = forms.ChangePasswordForm()

        # Password change form is submitted
        if password_form.validate_on_submit():
            if user.change_password(form=request.form):
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

    user = (db.session.query(models.User)
            .filter(models.User.username == username)
            .first_or_404(description="No matching user found"))
    
    authenticators.user_verification(user)

    # Create login form to check credentials
    form = forms.LoginForm()

    if form.validate_on_submit():

        search_username = request.form["username"]
        password = request.form["password"]

        search_user = (db.session.execute(select(models.User)
                       .filter_by(username=search_username))
                       .scalar())

        if search_user and authenticators.user_verification(search_user):
            if search_user.check_password(password):
                
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
                flash("Authentication failed, incorrect username or password")
                return redirect(url_for("user.user_page", username=current_user.username))
        else:
            flash("Authentication failed, incorrect username or password")
            return redirect(url_for("user.user_page", username=current_user.username))
    else:
        # Change LoginForm submit button text
        form.submit.label.text = "Terminate Contract"
        return render_template("pages/delete_user.html", form=form, user=user)


# Function called when recovering password
@bp.route("/user/request-password-reset", methods=["GET", "POST"])
@limiter.limit("3/day", methods=["POST"])
def request_password_reset():

    # Check if user is not logged in
    if not current_user.is_authenticated:

        form = forms.PasswordRecoveryForm()
        if form.validate_on_submit():
            
            email = request.form["email"].lower()
            user = (db.session.execute(select(models.User)
                    .filter_by(email=email))
                    .scalar())
            
            if user:
                messengers.send_recovery_email(recipient_email=email, user=user)
                flash(f"Account recovery email sent to {email}")
            else:
                flash("No account matching given email found. Please check your email address and try again")

        return render_template("pages/password_recovery.html",
                               form=form)
    
    else:
        return redirect(url_for("user.login"))
    

# Function called via recovery email url
@bp.route("/user/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token): 

    if current_user.is_authenticated:
        return redirect(url_for("campaign.campaigns"))
    
    # Verify that password reset token is valid
    user = models.User.verify_password_reset_token(token)
    if not user:
        flash("Token has either expired of is invalid")
        return redirect(url_for("home.home"))
    
    form = forms.ResetPasswordForm()

    if form.validate_on_submit():
        if user.change_password(form=request.form, reset=True):
            flash("Password updated, please login using new password")
        return redirect(url_for("user.login"))

    return render_template("pages/password_reset.html", form=form)
