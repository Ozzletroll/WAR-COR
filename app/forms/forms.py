from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, EmailField, SubmitField, PasswordField, \
                    BooleanField, FileField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, InputRequired, Optional, EqualTo, Length, Email

from app.forms.validators import *


class RegisterUserForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=30)])
    password = PasswordField("Password", validators=[DataRequired(), 
                                                     Length(min=8), 
                                                     EqualTo("confirm_password", message="Passwords must match")])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField("Sign Up")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(max=30)])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class PasswordRecoveryForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Recover")


class ChangeUsernameForm(FlaskForm):
    username = StringField("New Username", validators=[DataRequired(), Length(min=3, max=30)])
    submit = SubmitField("Update")


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField("Password", validators=[DataRequired()])
    new_password = PasswordField("New Password", 
                                 validators=[DataRequired(),
                                             Length(min=8),
                                             EqualTo("confirm_password",
                                                     message="Passwords must match")])
    confirm_password = PasswordField("Confirm Password")
    submit = SubmitField("Update")


class ResetPasswordForm(FlaskForm):
    new_password = PasswordField("New Password", 
                                 validators=[DataRequired(),
                                             Length(min=8),
                                             EqualTo("confirm_password", 
                                                     message="Passwords must match")])
    confirm_password = PasswordField("Confirm Password")
    submit = SubmitField("Update")


class CreateCampaignForm(FlaskForm):
    title = StringField("Campaign Title", validators=[DataRequired(), Length(max=250)])
    description = TextAreaField("Description", validators=[DataRequired(), Length(max=700)])
    date_suffix = StringField("Date Suffix", validators=[Optional()])
    negative_date_suffix = StringField("Negative Date Suffix", validators=[Optional()])
    submit = SubmitField("Create Campaign")


class CreateEventForm(FlaskForm):
    """ 
        The "edit_" prefix fields are rendered as hidden fields on the page,
        and toggled via Javascript when the user makes a change to the corresponding field.
        This helps prevent unnecessary overwrites if multiple users are editing
        the same model at once.
        
    """
    edit_title = BooleanField("Edit Title")
    edit_type = BooleanField("Edit Type")
    edit_date = BooleanField("Edit Date")
    edit_location = BooleanField("Edit Location")
    edit_belligerents = BooleanField("Edit Belligerents")
    edit_hide_time = BooleanField("Edit Hide Time")
    edit_body = BooleanField("Edit Body")
    edit_result = BooleanField("Edit Result")

    title = StringField("Event Title", validators=[DataRequired(), Length(max=250)])
    type = StringField("Event Type", validators=[DataRequired(), Length(max=250)])
    date = StringField("Event Date", validators=[InputRequired(), date_format(format="event")])
    location = StringField("Location", validators=[Optional()])
    belligerents = StringField("Belligerents", validators=[Optional()])
    body = TextAreaField("Body", validators=[DataRequired()])
    result = StringField("Result", validators=[Optional()])
    hide_time = BooleanField("Hide Time", default=False, validators=[Optional()])
    submit = SubmitField("Create Event")


class CreateEpochForm(FlaskForm):
    """ 
        The "edit_" prefix fields are rendered as hidden fields on the page,
        and toggled via Javascript when the user makes a change to the corresponding field.
        This helps prevent unnecessary overwrites if multiple users are editing
        the same model at once.
        
    """

    # Register custom validators for error collection
    class Meta:
        validators = {
            'start_date': [date_format(format="epoch")],
            'end_date': [date_format(format="epoch"), date_is_after]
        }

    edit_title = BooleanField("Edit Title")
    edit_start_date = BooleanField("Edit Start Date")
    edit_end_date = BooleanField("Edit End Date")
    edit_overview = BooleanField("Edit Overview")
    edit_description = BooleanField("Edit Description")

    title = StringField("Event Title", validators=[DataRequired(), Length(max=250)])
    start_date = StringField("Start Date", validators=[date_format(format="epoch")])
    end_date = StringField("End Date", validators=[date_format(format="epoch"), date_is_after])
    overview = TextAreaField("Overview")
    description = TextAreaField("Description")
    submit = SubmitField("Create Epoch")


class SearchUserForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    submit = SubmitField("Search")


class AddUserForm(FlaskForm):
    """ The name "submit_button" is used rather than "submit" as to avoid conflict 
        with javascript form.submit() funtion. """
    username = StringField("Username", validators=[DataRequired()])
    user_id = IntegerField("User ID", validators=[DataRequired()])
    submit_button = SubmitField("Invite")


class SubmitForm(FlaskForm):
    submit = SubmitField("Submit")


class ChangeCallsignForm(FlaskForm):
    callsign = StringField("New Callsign", validators=[DataRequired(), Length(max=30)])
    submit = SubmitField("Update")
    

class UploadJsonForm(FlaskForm):
    file = FileField("Backup JSON", validators=[DataRequired(), 
                                                FileAllowed(["json"], 
                                                            "Please select a valid WAR/COR JSON file"),
                                                file_format()])
    submit = SubmitField("Restore")


class CommentForm(FlaskForm):
    body = TextAreaField("Comment", validators=[DataRequired(), Length(max=300)])
    submit = SubmitField("Submit")


class SearchForm(FlaskForm):
    search = StringField("Search", validators=[Length(min=3)])
    submit = SubmitField("Search")
