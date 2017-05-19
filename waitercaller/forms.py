from flask_wtf import Form
from wtforms import PasswordField
from wtforms import SubmitField
from wtforms.fields.html5 import EmailField
from wtforms import validators

class RegistrationForm(Form):
    email = EmailField('email', validators = [validators.DataRequired(), validators.Email()])
    password = PasswordField('password', validators = [validators.DataRequired(), validators.Length(min=8, message="Please choose a password of atleast 8 characters")])
    password2 = PasswordField('password', validators = [validators.DataRequired(), validators.EqualTo('password', message="Passwords must match")])
    submit = SubmitField('submit', [validators.DataRequired()])
