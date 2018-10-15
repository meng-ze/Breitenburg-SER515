from wtforms import Form, StringField, PasswordField, TextAreaField, validators

# Register Form Class
class RegisterForm(Form):
    name_field = StringField('Name', [validators.DataRequired(), validators.Length(min=1, max=50)])
    email_field = StringField('Email', [validators.DataRequired(), validators.Length(min=6, max=50)])
    password_field = PasswordField('Password', [validators.DataRequired(), validators.EqualTo('confirm_field', message='Passwords do not match')])
    confirm_field = PasswordField('Confirm Password')

class LoginForm(Form):
    email_field = StringField('Email')
    password_field = PasswordField('Password')

class CreatePostForm(Form):
    title = StringField('Title', [validators.DataRequired(), validators.Length(min=1, max=50)])
    body = TextAreaField('Body', [validators.DataRequired(), validators.Length(min=1, max=5000)])