from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, RadioField
from wtforms.validators import DataRequired, Length


class CreateHeroForm(FlaskForm):
    h_name = StringField("Hero Name", validators=[DataRequired(), Length(min=3, max=16)])
    h_gender = RadioField("Choose gender", choices=[(0, "Male"), (1, "Female")], coerce=int, default=0)

    submit = SubmitField("Create")