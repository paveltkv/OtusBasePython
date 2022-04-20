from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired, Length


class UserForm(FlaskForm):
    name = StringField("Login", name="name", validators=[
        DataRequired(),
        Length(min=3),
    ])
    username = StringField("User name", name="username", validators=[
        DataRequired(),
        Length(min=3),
    ])
    email = StringField("Email", name="email", validators=[
        DataRequired(),
        Length(min=3),
    ])

