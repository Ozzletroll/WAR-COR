from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, SubmitField, PasswordField, BooleanField, FileField
from wtforms.validators import DataRequired, InputRequired, Optional, EqualTo, ValidationError, Length
from flask_ckeditor import CKEditorField
import re


# Custom validators
def date_format(format):

    if format == "event":
        message = "Not a valid date format, please use the format 'YYYY-MM-DD HH:MM:SS'"
        format = r"^\d{1,9}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$"
    elif format == "epoch":
        message = "Not a valid date format, please use the format 'YYYY-MM'"
        format = r"^\d{1,9}-\d{2}$"

    def _date_format(form, field):

        if not re.match(format, field.data):
            raise ValidationError(message)

    return _date_format


def file_format():

    def _file_format(form, field):

        # Check if filesize is below 5MB
        if field.data:
            max_size = 5 * 1024 * 1024  # 5MB
            if field.data.content_length > max_size:
                raise ValidationError('File size must be less than 5MB.')

    return _file_format


def date_is_after(form, field):
    start_date = form.start_date.data
    end_date = field.data

    start_year, start_month = map(int, start_date.split("-"))
    end_year, end_month = map(int, end_date.split("-"))

    if start_year > end_year or (start_year == end_year and start_month > end_month):
        raise ValidationError("End Date must be equal or greater than Start Date")


class RegisterUserForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(max=30)])
    password = PasswordField("Password", validators=[DataRequired(), EqualTo("confirm_password",
                                                                             message="Password must match")])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField("Sign Up")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(max=30)])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class ChangeUsernameForm(FlaskForm):
    username = StringField("New Username", validators=[DataRequired(), Length(max=30)])
    submit = SubmitField("Update")


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField("Password", validators=[DataRequired()])
    new_password = PasswordField('New Password', [DataRequired(), EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField("Confirm Password")
    submit = SubmitField("Update")


class CreateCampaignForm(FlaskForm):
    title = StringField("Campaign Title", validators=[DataRequired()])
    description = CKEditorField("Description", validators=[DataRequired()])
    date_suffix = StringField("Campaign Title", validators=[Optional()])
    submit = SubmitField("Create Campaign")


class CreateEventForm(FlaskForm):
    title = StringField("Event Title", validators=[DataRequired()])
    type = StringField("Event Type", validators=[DataRequired()])
    date = StringField("Event Date", validators=[InputRequired(), date_format(format="event")])
    location = StringField("Location", validators=[Optional()])
    belligerents = StringField("Belligerents", validators=[Optional()])
    body = CKEditorField("Body", validators=[DataRequired()])
    result = StringField("Result", validators=[Optional()])
    header = BooleanField("Header", default=False, validators=[Optional()])
    hide_time = BooleanField("Hide Time", default=False, validators=[Optional()])
    submit = SubmitField("Create Event")


class CreateEpochForm(FlaskForm):
    # Register custom validators for error collection
    class Meta:
        validators = {
            'start_date': [date_format(format="epoch")],
            'end_date': [date_format(format="epoch")]
        }

    title = StringField("Event Title", validators=[DataRequired()])
    start_date = StringField("Start Date", validators=[date_format(format="epoch")])
    end_date = StringField("End Date", validators=[date_format(format="epoch")])
    description = CKEditorField("Description")
    submit = SubmitField("Create Epoch")

class AddUserForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    submit = SubmitField("Search")


class ChangeCallsignForm(FlaskForm):
    callsign = StringField("New Callsign", validators=[DataRequired(), Length(max=30)])
    submit = SubmitField("Update")
    

class UploadJsonForm(FlaskForm):
    file = FileField("Backup JSON", validators=[DataRequired(), FileAllowed(["json"], "Please select a valid WAR/COR JSON file"), file_format()])
    submit = SubmitField("Restore")


class CommentForm(FlaskForm):
    body = CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField("Submit")


class CampaignSearchForm(FlaskForm):
    search = StringField("Search", validators=[Length(min=3)])
    submit = SubmitField("Search")
