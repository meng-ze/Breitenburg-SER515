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
        register_success = False

        if WebsiteAPI.is_user_exist(email, main_website) == False:
            info_package = {
                AccountInfo.EMAIL: email, 
                AccountInfo.PASSWORD: password, 
                AccountInfo.PHONE: '', 
                AccountInfo.DATE_OF_BIRTH: '', 
                AccountInfo.GENDER: 'M'
            } 
            register_success = WebsiteAPI.create_account(name, info_package, main_website)
        else:
            flash('User with this email id exists')

        if register_success:
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
        if len(all_posts) == 0:
            flash('No posts to display')
        return render_template('view.html', view_posts=all_posts)
    else:
        return render_template('index.html', title='View Post')


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == "POST":

        search_target = request.form['search']
        all_posts = WebsiteAPI.get_all_posts(main_website, inner_join=False, filter_dict={PostInfo.POST_TITLE: search_target})
        if len(all_posts) == 0:
            flash('No results Found!')

        return render_template('search.html', searched_posts=all_posts)  # <- Here you jump away from whatever result you create


@app.route('/my_posts', methods=['GET', 'POST'])
def my_posts():
    if session.get(WebsiteLoginStatus.LOGGED_IN) is None:
        session[WebsiteLoginStatus.LOGGED_IN] = False

    if session[WebsiteLoginStatus.LOGGED_IN] == True:
        logged_user_id = session[WebsiteLoginStatus.LOGGED_USER_ID]
        all_posts = WebsiteAPI.get_all_posts(main_website, inner_join=False, filter_dict={AccountInfo.USER_ID: logged_user_id})

        return render_template('my_posts.html', title='My Posts', posts=all_posts)
    else:
        return render_template('index.html', title='Home')


@app.route('/edit_post', methods=['GET', 'POST'])
def edit_post():
    if session.get('logged_in') is None:
        session['logged_in'] = False

    if session['logged_in'] == True:
        if request.method == 'POST':
            post_id = request.form[PostInfo.POST_ID]
            post = WebsiteAPI.get_all_posts(main_website, False, filter_dict={PostInfo.POST_ID: post_id})

        return render_template('edit_post.html', title='Edit Post', post=post)
    else:
        return render_template('index.html', title='Home')


# @app.route('/post')
# def post():
#     if session.get(WebsiteLoginStatus.LOGGED_IN) is None:
#         session[WebsiteLoginStatus.LOGGED_IN] = False

#     if session[WebsiteLoginStatus.LOGGED_IN] == True:
#         return render_template('post.html')
#     else:
#         return render_template('index.html', title='Post')


@app.route('/post', methods=['GET', 'POST'])
def post():
    if session.get('logged_in') is None:
        session['logged_in'] = False

    if session['logged_in'] == True:
        conn = main_website.mysql_server.connect()
        cur = conn.cursor()
        if request.method == 'POST':
            post_id = request.form['id']
            c = request.form['comment']
            cur.execute("INSERT INTO comment(post_id, user_id, comment_text) VALUES(%s, %s, %s)", (post_id, session['logged_user_id_num'], c))
            conn.commit()
        else:
            post_id = request.args.get('id')

        cur.execute('SELECT * FROM post WHERE post_id = %s', post_id)
        post = cur.fetchone()
        cur.execute('SELECT * FROM user WHERE user_id = %s', post[1])
        user = cur.fetchone()

        cur.execute('SELECT * FROM comment WHERE post_id = %s', post_id)
        result = cur.fetchall()
        comments = [list(i) for i in result]
        # Not sure if we need to sort by date, so remove comment if we need to
        # comments = sorted(comments, key=lambda comment: comment[4])
        for i, c in enumerate(comments):
            cur.execute('SELECT * FROM user where user_id = %s', c[2])
            commentUser = cur.fetchone()
            c.append(commentUser[1])
            comments[i] = c
        return render_template('post.html', post=post, comments=comments, user=(user[0], user[1]))
    else:
        return render_template('index.html', title='Post')


@app.route('/createPost' , methods=['GET', 'POST'])
def createPost():
    if session.get(WebsiteLoginStatus.LOGGED_IN) is None:
        session[WebsiteLoginStatus.LOGGED_IN] = False

    if session[WebsiteLoginStatus.LOGGED_IN] == True:
        form = CustomForm.CreatePostForm(request.form, main_website)
        if request.method == 'POST' and form.validate():
            
            title = form.title_field.data
            body = form.body_field.data
            category = request.form[DatabaseModel.CATEGORY]
            email = session[WebsiteLoginStatus.LOGGED_USER_EMAIL]

            create_post_status = WebsiteAPI.create_post(email, title, body, category, main_website)
            if create_post_status[0]:
                return redirect('/post?id=' + str(create_post_status[1]))
        
        categories = WebsiteAPI.get_category_list(main_website)
        return render_template('createPost.html', categories=categories, form=form)
    else:
        return render_template('index.html', title='Create Post')

### Admin feature
@app.route('/create_admin', methods=['GET', 'POST'])
def create_admin():
    form = CustomForm.RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name_field.data
        email = form.email_field.data
        password = form.password_field.data
        admin_create_success = False

        if WebsiteAPI.is_user_exist(email, main_website) == False:
            info_package = {
                AccountInfo.EMAIL: email, 
                AccountInfo.PASSWORD: password, 
                AccountInfo.USER_ROLE_ID: 2,
                AccountInfo.PHONE: '', 
                AccountInfo.DATE_OF_BIRTH: '', 
                AccountInfo.GENDER: '-'
            } 
            admin_create_success = WebsiteAPI.create_account(name, info_package, main_website)

        else:
            flash('User with this email id exists')

        if admin_create_success:
            flash('New Admin created successfully')
            return redirect(url_for('create_admin'))
    return render_template('create_admin.html', title='Get Registered', form=form)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')