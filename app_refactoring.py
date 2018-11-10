from flask import Flask, render_template, redirect, url_for, request, flash, session
#from data import Articles
from Website import Website
from flaskext.mysql import MySQL
from wtforms import Form, StringField, PasswordField, TextAreaField, validators
import CustomForm
import WebsiteAPI
from ConstantTable import DatabaseModel, AccountInfo, PostInfo, WebsiteLoginStatus 

import time, datetime

app = Flask(__name__)
mysql_server = MySQL()
main_website = Website(app, mysql_server)

@app.route('/')
def index():
    if session.get(WebsiteLoginStatus.LOGGED_IN) is None:
        session[WebsiteLoginStatus.LOGGED_IN] = False
    all_posts = WebsiteAPI.get_all_posts(main_website)
    if len(all_posts) == 0:
        flash('No posts to display')

    return render_template('index.html', view_posts=all_posts)

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
    if session.get(WebsiteLoginStatus.LOGGED_IN) is None:
        session[WebsiteLoginStatus.LOGGED_IN] = False

    session[WebsiteLoginStatus.LOGGED_IN] = False
    session[WebsiteLoginStatus.LOGGED_USER_EMAIL] = ""
    session[WebsiteLoginStatus.LOGGED_USER_ID] = 0
    session[WebsiteLoginStatus.LOGGED_USER_ROLE_ID] = 0
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = CustomForm.LoginForm(request.form, main_website)
    if request.method == 'POST' and form.validate():
        email = form.email_field.data
        password = form.password_field.data

        login_success = WebsiteAPI.verify_login_password(email, password, main_website)
        if not login_success[0]:
            flash('Incorrect username/password.')
        else:
            session[WebsiteLoginStatus.LOGGED_IN] = True
            session[WebsiteLoginStatus.LOGGED_USER_EMAIL] = login_success[1][AccountInfo.EMAIL]
            session[WebsiteLoginStatus.LOGGED_USER_ID] = login_success[1][AccountInfo.USER_ID]
            session[WebsiteLoginStatus.LOGGED_USER_ROLE_ID] = login_success[1][AccountInfo.USER_ROLE_ID]
            flash('You were successfully logged in')
            return redirect(url_for('view'))
    return render_template('login.html', title='Login', form=form)


@app.route('/view')
def view():
    if session.get(WebsiteLoginStatus.LOGGED_IN) is None:
        session[WebsiteLoginStatus.LOGGED_IN] = False

    if session[WebsiteLoginStatus.LOGGED_IN] == True:
        all_posts = WebsiteAPI.get_all_posts(main_website, order='{}.{}'.format(DatabaseModel.POST, PostInfo.TIMESTAMP))
        # print(view_posts)
        if len(all_posts) == 0:
            flash('No posts to display')
        return render_template('view.html', view_posts=all_posts)
    else:
        return render_template('index.html', title='View Post')


@app.route('/post')
def post():
    if session.get(WebsiteLoginStatus.LOGGED_IN) is None:
        session[WebsiteLoginStatus.LOGGED_IN] = False

    if session[WebsiteLoginStatus.LOGGED_IN] == True:
        return render_template('post.html')
    else:
        return render_template('index.html', title='Post')

@app.route('/createPost' , methods=['GET', 'POST'])
def createPost():
    if session.get(WebsiteLoginStatus.LOGGED_IN) is None:
        session[WebsiteLoginStatus.LOGGED_IN] = False

    if session[WebsiteLoginStatus.LOGGED_IN] == True:
        form = CustomForm.CreatePostForm(request.form, main_website)
        if request.method == 'POST' and form.validate():
            
            timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
            title = form.title.data
            body = form.body.data
            category = request.form[DatabaseModel.CATEGORY]
            email = session[WebsiteLoginStatus.LOGGED_USER_EMAIL]

            post_create_success = WebsiteAPI.create_post(email, title, body, category, timestamp, main_website)
            if post_create_success:
                return render_template('post.html')
        
        categories = WebsiteAPI.get_category_list(main_website)
        return render_template('createPost.html', categories=categories, form = form)
    else:
        return render_template('index.html', title='Create Post')

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')
    