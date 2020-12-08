from flask_wtf import Form
from wtforms import StringField, PasswordField,SubmitField, BooleanField
from wtforms.validators import DataRequired, Length
from wtforms.widgets import PasswordInput


class AddPasswordField(Form):
    website = StringField('Website',validators=[DataRequired(), Length(min=1)])
    email = StringField('Email', validators=[DataRequired(), Length(min=1)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=1)],widget=PasswordInput(hide_value=False))
    submit = SubmitField('Submit')

class Login(Form):
    username = StringField('Username',validators=[DataRequired(), Length(min=1)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=1)],widget=PasswordInput(hide_value=True))
    rememberMe = BooleanField('Remember Me')

class Signup(Form):
    username = StringField('Username',validators=[DataRequired(), Length(min=1)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=1)],widget=PasswordInput(hide_value=True))


