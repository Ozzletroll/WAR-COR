from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField, DateTimeField
from wtforms.validators import DataRequired, InputRequired, EqualTo
from flask_ckeditor import CKEditorField


# User management forms
class RegisterUserForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), EqualTo("confirm_password",
                                                                             message="Password must match")])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField("Sign Up")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class ChangeUsernameForm(FlaskForm):
    new_username = StringField("New Username", validators=[DataRequired()])
    submit = SubmitField("Update")


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField("Password", validators=[DataRequired()])
    new_password = PasswordField('New Password', [DataRequired(), EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField("Confirm Password")
    submit = SubmitField("Update")


class CreateCampaignForm(FlaskForm):
    title = StringField("Campaign Title", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])
    submit = SubmitField("Create Campaign")


class CreateEventForm(FlaskForm):
    title = StringField("Event Title", validators=[DataRequired()])
    type = StringField("Event Type", validators=[DataRequired()])
    date = DateTimeField("Event Date", format='%Y-%m-%d %H:%M:%S', validators=[InputRequired()])
    location = StringField("Location", validators=[DataRequired()])
    belligerents = StringField("Belligerents", validators=[DataRequired()])
    body = TextAreaField("Description", validators=[DataRequired()])
    result = StringField("Result", validators=[DataRequired()])
    submit = SubmitField("Create Event")


class AddUserForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    submit = SubmitField("Add user")


class ChangeCallsignForm(FlaskForm):
    callsign = StringField("New Callsign", validators=[DataRequired()])
    submit = SubmitField("Update")
    