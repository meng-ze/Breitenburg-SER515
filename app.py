from flask import Flask, render_template, redirect, url_for, request, flash, session
#from data import Articles
from Website import Website
from flaskext.mysql import MySQL
from wtforms import Form, StringField, PasswordField, TextAreaField, validators
import CustomForm
import WebsiteAPI
from ConstantTable import AccountInfo

import time, datetime

app = Flask(__name__)
mysql_server = MySQL()
main_website = Website(app, mysql_server)

@app.route('/')
def index():
    if session.get('logged_in') is None:
        session['logged_in'] = False
    return render_template('index.html')

# User Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = CustomForm.RegisterForm(request.form, main_website)
    if request.method == 'POST' and form.validate():
        name = form.name_field.data
        email = form.email_field.data
        password = form.password_field.data

        info_package = {
            AccountInfo.EMAIL: email, 
            AccountInfo.PASSWORD: password, 
            AccountInfo.PHONE: '', 
            AccountInfo.DATE_OF_BIRTH: '', 
            AccountInfo.GENDER: 'M'
        } 
        register_flag = WebsiteAPI.create_account(name, info_package, main_website)

        if register_flag:
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
    form = CustomForm.LoginForm(request.form, main_website)
    if request.method == 'POST' and form.validate():
        email = form.email_field.data
        password = form.password_field.data

        login_success = WebsiteAPI.verify_login_password(email, password, main_website)
        if not login_success:
            flash('Incorrect username/password.')
        else:
            session['logged_in'] = True
            session['logged_user_id'] = form.email_field.data
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

# Post Form Class
class CreatePostForm(Form):
    title = StringField('Title', [validators.DataRequired(), validators.Length(min=1, max=50)])
    body = TextAreaField('Body', [validators.DataRequired(), validators.Length(min=1, max=5000)])
    

@app.route('/createPost' , methods=['GET', 'POST'])
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
        
        return render_template('createPost.html', categories=categories, form = form)
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
    app.run(debug=True, host='127.0.0.1')
    