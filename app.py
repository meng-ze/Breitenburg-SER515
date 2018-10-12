from flask import Flask, render_template, redirect, url_for, request, flash, session
#from data import Articles
from flaskext.mysql import MySQL
from wtforms import Form, StringField, PasswordField, TextAreaField, validators


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

# search class


class Post(Form):
    title = StringField('Post Title')
    desc = StringField('Decription')


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
    session['logged_user_id'] = ""
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
            session['logged_user_id'] = form.email.data
            flash('You were successfully logged in')
            return redirect(url_for('view'))
    return render_template('login.html', title='Login', form=form)


@app.route('/view', methods=['GET', 'POST'])
def view():
    if session.get('logged_in') is None:
        session['logged_in'] = False

    if session['logged_in'] == True:
        search = Post(request.form)
        if request.method == 'POST':
            returnsearch_results(search)
        return render_template('view.html', form=search)
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

# Post Form Class


class CreatePostForm(Form):
    title = StringField('Title', [validators.DataRequired(), validators.Length(min=1, max=50)])
    body = TextAreaField('Body', [validators.DataRequired(), validators.Length(min=1, max=5000)])


@app.route('/createPost', methods=['GET', 'POST'])
def createPost():
    if session.get('logged_in') is None:
        session['logged_in'] = False

    if session['logged_in'] == True:
        form = CreatePostForm(request.form)
        if request.method == 'POST' and form.validate():

            title = form.title.data
            body = form.body.data
            category = request.form["category"]
            user_id = session['logged_user_id']
            # write code to insert values in database here

            return render_template('post.html')

        conn = mysql.connect()
        cur = conn.cursor()
        cur.execute("SELECT * FROM category")
        categories = []
        for (category) in cur:
            categories.append(category)
        cur.close()

        return render_template('createPost.html', categories=categories, form=form)
    else:
        return render_template('index.html', title='Create Post')


# new changes -- aneesh to work on this.


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == "POST":
        conn = mysql.connect()
        cur = conn.cursor()
        cur.execute('''select post_title from Post where post_title = %s''', request.form['search'])
        result = cur.fetchall()
        searched_posts = [list(i) for i in result]

        return redirect(url_for('search'))  # <- Here you jump away from whatever result you create
    return render_template('view.html')


def getCategoryList():
    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM category")
    result = cur.fetchall()
    category_list = [list(i) for i in result]

    return category_list


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
