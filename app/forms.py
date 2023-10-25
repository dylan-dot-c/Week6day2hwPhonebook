from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SubmitField
from wtforms.validators import InputRequired

class ContactForm(FlaskForm):
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    phone_number = StringField('Phone', validators=[InputRequired()])
    email = EmailField('Email', validators=[InputRequired()])
    address = StringField('Content', validators=[InputRequired()])
    submit = SubmitField('Add New Contact ')