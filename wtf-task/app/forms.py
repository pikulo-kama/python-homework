from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class ContactForm(FlaskForm):
    name = StringField('Name',
                       validators=[DataRequired(message="Field can't be empty")],
                       render_kw={'size': 31})

    email = StringField('Email',
                        validators=[
                            DataRequired(),
                            Email(message='Incorrect email address!')],
                        render_kw={'size': 31})

    body = TextAreaField('Body',
                         validators=[
                             DataRequired(),
                             Length(min=20, max=255, message="Possible range of characters [20:255]")],
                         render_kw={'cols': 35, 'rows': 5})

    submit = SubmitField('Submit')
