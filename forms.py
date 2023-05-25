from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField, DateTimeField
from wtforms.validators import DataRequired, URL, Email, EqualTo
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


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField("Password", validators=[DataRequired()])
    password = PasswordField('New Password', [DataRequired(), EqualTo('submit', message='Passwords must match')])
    submit = PasswordField('Repeat Password')


class CreateCampaignForm(FlaskForm):
    title = StringField("Campaign Title", validators=[DataRequired()])
    description = StringField("Description", validators=[DataRequired()])
    submit = SubmitField("Create Campaign")


class CreateEventForm(FlaskForm):
    title = StringField("Event Title", validators=[DataRequired()])
    type = StringField("Event Type", validators=[DataRequired()])
    date = DateTimeField("Event Date. Year-Month-Day Hours:Minutes:Seconds Format",
                         format='%Y-%m-%d %H:%M:%S', validators=[DataRequired()])
    location = StringField("Location", validators=[DataRequired()])
    belligerents = StringField("Belligerents", validators=[DataRequired()])
    body = StringField("Description", validators=[DataRequired()])
    result = StringField("Result", validators=[DataRequired()])
    submit = SubmitField("Create Event")


class AddUserForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    submit = SubmitField("Add user")
