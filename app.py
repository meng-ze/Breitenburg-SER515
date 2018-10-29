# pip install python-dateutil
from dateutil.parser import parse
from flask import Flask, render_template, redirect, url_for, request, flash, session
#from data import Articles
from flaskext.mysql import MySQL
from wtforms import Form, StringField, PasswordField, TextAreaField, validators
from wtforms.fields.html5 import EmailField

import time
import datetime


mysql = MySQL()
app = Flask(__name__, static_url_path='/static')

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

    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute('''SELECT * from post inner join user on post.user_id = user.user_id''')
    result = cur.fetchall()
    view_posts = [list(i) for i in result]
    # print(view_posts)
    if len(view_posts) is 0:
        flash('No posts to display')
    else:
        print('to check if itw working')
    return render_template('index.html', view_posts=view_posts)


# Register Form Class
class RegisterForm(Form):
    name = StringField('Name', [validators.DataRequired(), validators.Length(min=1, max=50)])
    email = EmailField('Email', [validators.DataRequired(), validators.Length(min=6, max=50), validators.Email()])
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

# Create Admin Form
class CreateAdminForm(Form):
    name = StringField('Name', [validators.DataRequired(), validators.Length(min=1, max=50)])
    email = EmailField('Email', [validators.DataRequired(), validators.Length(min=6, max=50), validators.Email()])
    password = PasswordField('Password', [validators.DataRequired(), validators.EqualTo('confirm', message='Passwords do not match')])
    confirm = PasswordField('Confirm Password')

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
        cur.execute("INSERT INTO user(username, email_id, password, phone, dob, gender) VALUES(%s, %s, %s, %s, %s, %s)", (name, email, password, "", "", 'M'))
        conn.commit()
        register_flag = 1
        cur.close()
        print(email, password)

        if register_flag == 1:
            flash('You have registered successfully')
            return redirect(url_for('login'))
    return render_template('register.html', title='Get Registered', form=form)


@app.route('/create_admin', methods=['GET', 'POST'])
def create_admin():
    form = CreateAdminForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        register_flag = 0

        conn = mysql.connect()
        cur = conn.cursor()
        
        
        number_of_rows= cur.execute("SELECT * FROM user WHERE email_id = %s", (email))
        if(number_of_rows == 0):
            cur.execute("INSERT INTO user(username, email_id, user_role, password, phone, dob, gender) VALUES(%s, %s, %s, %s, %s, %s, %s)", (name, email, "2", password, "", "", '-'))
            conn.commit()
            register_flag = 1
            cur.close()
        else:
            flash('User with the following email id exists')

        if register_flag == 1:
            flash('New Admin created successfully')
            return redirect(url_for('create_admin'))
    return render_template('create_admin.html', title='Get Registered', form=form)


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
        cur.execute("SELECT * FROM user inner join user_role on user.user_role = user_role.id WHERE email_id = %s and password = %s", (email, password))
        user_role_id = 0
        for (row) in cur:
            user_role_id = row[10] 
            flag = 1

        cur.close()
        if flag == 0:
            flash('Incorrect username/password.')
        else:
            session['role'] = user_role_id
            session['logged_in'] = True
            session['logged_user_id'] = form.email.data
            flash('You were successfully logged in')
            return redirect(url_for('view'))
    return render_template('login.html', title='Login', form=form)


@app.route('/my_posts', methods=['GET', 'POST'])
def my_posts():
    if session.get('logged_in') is None:
        session['logged_in'] = False

    if session['logged_in'] == True:
        conn = mysql.connect()
        cur = conn.cursor()
        
        cur.execute('''SELECT * from post where user_id = (Select user_id from user where email_id = %s Limit 1)''', (session['logged_user_id']))
        result = cur.fetchall()
        posts = [list(i) for i in result]
        

        return render_template('my_posts.html', title='My Posts', posts=posts)
    else:
        return render_template('index.html', title='Home')


@app.route('/edit_post', methods=['GET', 'POST'])
def edit_post():
    if session.get('logged_in') is None:
        session['logged_in'] = False

    if session['logged_in'] == True:
        if request.method == 'POST':
            post_id = request.form['post_id']
            print(post_id)
            conn = mysql.connect()
            cur = conn.cursor()
            cur.execute('''SELECT * from post where post_id = %s''', (post_id))
            result = cur.fetchone()
            post = result

        return render_template('edit_post.html', title='Edit Post', post=post)
    else:
        return render_template('index.html', title='Home')


@app.route('/view', methods=['GET', 'POST'])
def view():
    if session.get('logged_in') is None:
        session['logged_in'] = False

    if session['logged_in'] == True:
        conn = mysql.connect()
        cur = conn.cursor()
        cur.execute('''select * from Post inner join user on post.user_id = user.user_id order by post.timestamp desc''')
        result = cur.fetchall()
        view_posts = [list(i) for i in result]
        # print(view_posts)
        if len(view_posts) is 0:
            flash('No posts to display')
        else:
            print('to check if it working')
        return render_template('view.html', view_posts=view_posts)
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

            timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
            title = form.title.data
            body = form.body.data
            category = request.form["category"]
            user_email = session['logged_user_id']

            conn = mysql.connect()
            cur = conn.cursor()
            cur.execute("SELECT * FROM user WHERE email_id = %s", (user_email))
            for (user) in cur:
                user_id = str(user[0])
            conn = mysql.connect()
            cur = conn.cursor()
            cur.execute("INSERT INTO post(category_id, post_text, post_title, timestamp, user_id) VALUES(%s, %s, %s, %s, %s)", (category, body, title, timestamp, user_id))
            conn.commit()

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
        cur.execute('''SELECT * from post inner join user on post.user_id = user.user_id where post_title = %s''', (request.form['search']))
        result = cur.fetchall()
        searched_posts = [list(i) for i in result]
        # print(searched_posts)
        if len(searched_posts) is 0:
            flash('No results Found!')
        else:
            print
        return render_template('search.html', searched_posts=searched_posts)  # <- Here you jump away from whatever result you create
   # return render_template('view.html')



@app.route('/list_admin', methods=['GET', 'POST'])
def list_admin():
    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute('''SELECT * from user where user_role = 2''')
    result = cur.fetchall()
    admins_list = [list(i) for i in result]
    
    return render_template('list_admin.html',admins_list=admins_list)  # <- Here you jump away from whatever result you create
   # return render_template('view.html')



def getCategoryList():
    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM category")
    result = cur.fetchall()
    category_list = [list(i) for i in result]

    return category_list


if __name__ == '__main__':

    app.run(debug=True, host='0.0.0.0')
