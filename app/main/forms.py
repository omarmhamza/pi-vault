from flask_wtf import Form
from wtforms import StringField, PasswordField, FieldList, SelectField, SubmitField
from wtforms.validators import DataRequired, Email

class AddPasswordField(Form):
    website = StringField('Website',validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')



