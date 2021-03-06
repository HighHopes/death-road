from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError

from core.models import Subscription


class SubscriptionForm(FlaskForm):
    email = StringField("email", validators=[DataRequired(), Email()])
    submit = SubmitField("Subscribe")

    def validate_email(self, email):
        email = Subscription.query.filter_by(email=email.data).first()

        if email:
            raise ValidationError("This email is already in the subscription list.")
