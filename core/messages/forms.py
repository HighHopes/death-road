from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length


class SendMessageForm(FlaskForm):
    send_to = StringField("Username", validators=[DataRequired(), Length(min=3)])
    subject = StringField("Subject", validators=[Length(max=32)])
    msg_body = TextAreaField("Message")

    submit = SubmitField("Send")


class DeleteSingleMessageButton(FlaskForm):
    submit_del = SubmitField("Delete")


class MessageMultipleDelete(FlaskForm):
    multi_del = BooleanField()
    submit_del = SubmitField("Delete Selected")
