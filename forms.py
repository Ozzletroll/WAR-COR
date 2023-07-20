from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, InputRequired, Optional, EqualTo, ValidationError
from flask_ckeditor import CKEditorField
import re


# Custom validators
def date_format():

    message = "Not a valid date format, please use the format 'YYYY-MM-DD HH:MM:SS'"
    format = r"^\d{1,9}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$"

    def _date_format(form, field):

        if not re.match(format, field.data):
            raise ValidationError(message)

    return _date_format


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
    date_suffix = StringField("Campaign Title", validators=[Optional()])
    submit = SubmitField("Create Campaign")


class CreateEventForm(FlaskForm):
    title = StringField("Event Title", validators=[DataRequired()])
    type = StringField("Event Type", validators=[DataRequired()])
    date = StringField("Event Date", validators=[InputRequired(), date_format()])
    location = StringField("Location", validators=[DataRequired()])
    belligerents = StringField("Belligerents", validators=[DataRequired()])
    body = TextAreaField("Description", validators=[DataRequired()])
    result = StringField("Result", validators=[DataRequired()])
    header = BooleanField("Header", default=False, validators=[Optional()])
    submit = SubmitField("Create Event")


class AddUserForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    submit = SubmitField("Search")


class ChangeCallsignForm(FlaskForm):
    callsign = StringField("New Callsign", validators=[DataRequired()])
    submit = SubmitField("Update")
    
