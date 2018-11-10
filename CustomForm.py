from wtforms import Form, StringField, PasswordField, TextAreaField, validators
from wtforms.fields.html5 import EmailField

# Register Form Class
class RegisterForm(Form):
    name_field = StringField('Name', [validators.DataRequired(), validators.Length(min=1, max=50)])
    email_field = EmailField('Email', [validators.DataRequired(), validators.Length(min=6, max=50)])
    password_field = PasswordField('Password', [validators.DataRequired(), validators.EqualTo('confirm_field', message='Passwords do not match')])
    confirm_field = PasswordField('Confirm Password')

class LoginForm(Form):
    email_field = StringField('Email')
    password_field = PasswordField('Password')

class CreatePostForm(Form):
    title = StringField('Title', [validators.DataRequired(), validators.Length(min=1, max=50)])
    body = TextAreaField('Body', [validators.DataRequired(), validators.Length(min=1, max=5000)])

class CreateAdminForm(Form):
    name_field = StringField('Name', [validators.DataRequired(), validators.Length(min=1, max=50)])
    email_field = EmailField('Email', [validators.DataRequired(), validators.Length(min=6, max=50), validators.Email()])
    password_field = PasswordField('Password', [validators.DataRequired(), validators.EqualTo('confirm_field', message='Passwords do not match')])
    confirm_field = PasswordField('Confirm Password')