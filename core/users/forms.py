from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField, PasswordField, BooleanField, SelectField
from wtforms.validators import DataRequired, Email, Length, ValidationError, EqualTo

from core.models import User


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=32)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])

    submit = SubmitField("Sing Up")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()

        if user:
            raise ValidationError("Username is taken. Please choose another username.")

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()

        if email:
            raise ValidationError("E-mail is taken. Please choose another username.")


class UpdateAccount(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=32)])
    email = StringField("Email", validators=[DataRequired(), Email()])

    hidemail_checkbox = BooleanField('Hide your email')
    msg_per_page = SelectField("Show messages per page", choices=[(5, "5"), (10, "10"), (25, "25")], coerce=int)

    submit = SubmitField("Update Profile")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=32)])
    password = PasswordField("Password", validators=[DataRequired()])

    submit = SubmitField("Login")
