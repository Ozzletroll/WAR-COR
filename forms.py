from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField
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
