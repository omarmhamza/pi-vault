from flask_wtf import Form
from wtforms import StringField, PasswordField, FieldList, SelectField, SubmitField
from wtforms.validators import DataRequired, Email,URL
from wtforms.widgets import PasswordInput


class AddPasswordField(Form):
    website = StringField('Website',validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()],widget=PasswordInput(hide_value=False))
    submit = SubmitField('Submit')



