from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, Length


class PostForm(FlaskForm):
    title = StringField("Title", name="title", validators=[
        DataRequired(),
        Length(min=3),
    ])
    body = StringField("Text", name="body", validators=[
        DataRequired(),
        Length(min=3),
    ])
    user_id = IntegerField("user id", name="userid", validators=[
        DataRequired(),
    ])
