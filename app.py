from flask import Flask, render_template,  redirect, url_for,  request
#from data import Articles
from flaskext.mysql import MySQL
from wtforms import Form, StringField, PasswordField, validators


mysql = MySQL()
app = Flask(__name__)

# Config MySQL
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root123'
app.config['MYSQL_DATABASE_DB'] = 'web_forum'
app.secret_key = 'super secret key'
mysql.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')


# Register Form Class
class RegisterForm(Form):
    name = StringField('Name')
    username = StringField('Username')
    email = StringField('Email')
    password = PasswordField('Password')


# User Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        password = form.password.data


        conn = mysql.connect()
        cur = conn.cursor()
        cur.execute("INSERT INTO user(username, emailid, password, phone, dob, gender) VALUES(%s, %s, %s, %s, %s, %s)", (name, email, password, "","",'M'))
        conn.commit()
        cur.close()
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
