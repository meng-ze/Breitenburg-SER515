from wtforms import Form, StringField, PasswordField, TextAreaField, validators

# Register Form Class
class RegisterForm(Form):
    def __init__(self, formdata, website):
        self.name_field = StringField('Name', [validators.DataRequired(), validators.Length(min=1, max=50)])
        self.email_field = StringField('Email', [validators.DataRequired(), validators.Length(min=6, max=50)])
        self.password_field = PasswordField('Password', [validators.DataRequired(), validators.EqualTo('confirm', message='Passwords do not match')])
        self.confirm_field = PasswordField('Confirm Password')

class LoginForm(Form):
    def __init__(self, formdata, website):
        self.email_field = StringField('Email')
        self.password_field = PasswordField('Password')

class CreatePostForm(Form):
    def __init__(self, formdata, website):
        self.title = StringField('Title', [validators.DataRequired(), validators.Length(min=1, max=50)])
        self.body = TextAreaField('Body', [validators.DataRequired(), validators.Length(min=1, max=5000)])