from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField
from wtforms.validators import DataRequired, URL, Email, EqualTo
from flask_ckeditor import CKEditorField


class RegisterUserForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), EqualTo("confirm_password",
                                                                             message="Password must match")])
    confirm_password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign Up")
