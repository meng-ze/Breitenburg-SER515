from flask import Flask, render_template, redirect, url_for, request, flash, session
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
    if session.get('logged_in') is None:
        session['logged_in'] = False
    return render_template('index.html')


# Register Form Class
class RegisterForm(Form):
    name = StringField('Name', [validators.DataRequired(), validators.Length(min=1, max=50)])
    email = StringField('Email', [validators.DataRequired(), validators.Length(min=6, max=50)])
    password = PasswordField('Password', [validators.DataRequired(), validators.EqualTo('confirm', message='Passwords do not match')])
    confirm = PasswordField('Confirm Password')

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

        if register_flag == 1:
            flash('You have registered successfully')
            return redirect(url_for('login'))
    return render_template('register.html', title='Get Registered', form=form)

# User login


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if session.get('logged_in') is None:
        session['logged_in'] = False

    session['logged_in'] = False
    return render_template('index.html')


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
            session['logged_in'] = True
            flash('You were successfully logged in')
            return redirect(url_for('view'))
    return render_template('login.html', title='Login', form=form)


@app.route('/view')
def view():
    if session.get('logged_in') is None:
        session['logged_in'] = False

    if session['logged_in'] == True:
        return render_template('view.html')
    else:
        return render_template('index.html', title='View Post')


@app.route('/post')
def post():
    if session.get('logged_in') is None:
        session['logged_in'] = False

    if session['logged_in'] == True:
        return render_template('post.html')
    else:
        return render_template('index.html', title='Post')


@app.route('/createPost')
def createPost():
    if session.get('logged_in') is None:
        session['logged_in'] = False

    if session['logged_in'] == True:
        category_list = getCategoryList()
        print(category_list)
        return render_template('createPost.html', category_list = category_list)
    else:
        return render_template('index.html', title='Create Post')



def getCategoryList():
    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM category")
    result = cur.fetchall()
    category_list = [list(i) for i in result]
    
    return category_list

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
    