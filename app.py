from flask import Flask, render_template, redirect, url_for, request, flash
#from data import Articles
from flaskext.mysql import MySQL
from wtforms import Form, StringField, PasswordField, validators


mysql = MySQL()
app = Flask(__name__)

# Config MySQL
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
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

# Login Form Class


class LoginForm(Form):
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
        register_flag = 0

        conn = mysql.connect()
        cur = conn.cursor()
        cur.execute("INSERT INTO user(username, emailid, password, phone, dob, gender) VALUES(%s, %s, %s, %s, %s, %s)", (name, email, password, "", "", 'M'))
        conn.commit()
        register_flag = 1
        cur.close()
        
        if register_flag == 1 :
            flash('You have registered successfully')
            return redirect(url_for('index'))
    return render_template('register.html', form=form)

# User login


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        email = form.email.data
        password = form.password.data
        flag = 0

        conn = mysql.connect()
        cur = conn.cursor()
        cur.execute("SELECT * FROM user WHERE emailid = %s and password = %s", (email, password))

        for (emailid) in cur:
            print("{}".format(emailid))
            flag = 1

        cur.close()
        if flag == 0:
            flash('Incorrect username/password.')
        else:
            flash('You were successfully logged in')
            return redirect(url_for('index'))
    return render_template('login.html', form=form)


@app.route('/view')
def view():
    return render_template('view.html')

@app.route('/post')
def post():
    return render_template('post.html')

@app.route('/createPost')
def createPost():
    return render_template('createPost.html')

if __name__ == '__main__':
    app.run(debug=True)
