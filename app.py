# pip install python-dateutil
from dateutil.parser import parse
import secrets
import os
#from PIL import Image
from flask import Flask, render_template, redirect, url_for, request, flash, session
#from data import Articles
from flaskext.mysql import MySQL
from wtforms import Form, StringField, PasswordField, TextAreaField, validators, DateField, DateTimeField, FileField
from wtforms.fields.html5 import EmailField
from werkzeug.utils import secure_filename

import time
import datetime


mysql = MySQL()
app = Flask(__name__, static_url_path='/static')

# config for profile pic
UPLOAD_FOLDER = 'C:\\Users\\ganga\\Desktop\\Project Sunday\\Breitenburg-SER515\\static\\profile_pics'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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

# create Update Account Form


class UpdateAccountForm(Form):
    name = StringField('Name', [validators.DataRequired(), validators.Length(min=1, max=50)])
    password = PasswordField('Password')
    email = EmailField('Email', [validators.DataRequired(), validators.Length(min=6, max=50), validators.Email()])
    dob = StringField('Date of birth')
    address = StringField('Address', [validators.DataRequired(), validators.Length(min=6, max=150)])
    phone = StringField('Phone', [validators.Length(min=10, max=10)])
    work = StringField('Work', [validators.Length(min=6, max=100)])
    education = StringField('Education', [validators.Length(min=6, max=150)])
    details = StringField('Other details', [validators.Length(min=6, max=250)])
    picture = FileField('Update Profile Picture')

# picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
# submit = SubmitField('Update')

# def validate_username(self, username):
#     if username.data != current_user.username:
#         user = User.query.filter_by(username=username.data).first()
#         if user:
#             raise ValidationError('That username is taken. Please choose a different one.')


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

        number_of_rows = cur.execute("SELECT * FROM user WHERE email_id = %s", email)
        if number_of_rows == 0:
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


@app.route('/name_click', methods=['GET', 'POST'])
def name_click():
    if request.method == 'GET':
        print(request.args['user'])

        if session.get('logged_in') is None:
            session['logged_in'] = False

        if session['logged_in']:
            conn = mysql.connect()
            cur = conn.cursor()

            cur.execute("SELECT username,email_id,dob,address,phone,work,education,about,profile_picture FROM user WHERE username = %s", request.args['user'])
            result = cur.fetchall()
            results = [list(i) for i in result]

            for item in results:
                print(item[0])
                print(item[1])
                print(item[2])
                print(item[3])
                print(item[4])
                if item[8]:
                    full_profilepic_path = "..\\static\\profile_pics\\" + item[8]
                else:
                    full_profilepic_path = "..\\static\\profile_pics\\default.jpg"
            return render_template('ViewProfile.html', title='Profile', posts=results, full_profilepic_path=full_profilepic_path)
        else:
            return render_template('index.html', title='Home')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/account', methods=['GET', 'POST'])
def account():
    form = UpdateAccountForm(request.form)
    if request.method == 'GET':
        if session.get('logged_in') is None:
            session['logged_in'] = False

        if session['logged_in']:
            conn = mysql.connect()
            cur = conn.cursor()

            cur.execute("SELECT username,email_id,dob,address,phone,work,education,about,profile_picture FROM user WHERE email_id = %s", (session['logged_user_id']))
            result = cur.fetchall()
            results = [list(i) for i in result]

            for item in results:
                form.name.data = item[0]
                form.email.data = item[1]
                form.dob.data = item[2]
                form.address.data = item[3]
                form.phone.data = item[4]
                form.work.data = item[5]
                form.education.data = item[6]
                form.details.data = item[7]
                form.picture.data = item[8]
                if item[8]:
                    full_profilepic_path = "..\\static\\profile_pics\\" + item[8]
                else:
                    full_profilepic_path = "..\\static\\profile_pics\\default.jpg"
                # print(full_profilepic_path)
            return render_template('account.html', title='My Profile', form=form, full_profilepic_path=full_profilepic_path)
        else:
            return render_template('index.html', title='Home')

    if request.method == 'POST':
        # print("YAY")
        name = form.name.data
        dob = form.dob.data
        address = form.address.data
        phone = form.phone.data
        work = form.work.data
        education = form.education.data
        details = form.details.data

        conn = mysql.connect()
        cur = conn.cursor()

        cur.execute("SELECT profile_picture FROM user WHERE email_id = %s", (session['logged_user_id']))
        results = cur.fetchall()
        for item in results:
            form.picture.data = item[0]
        conn.commit()
        cur.close()
        if form.picture.data is None:
            full_profilepic_path = "..\\static\\profile_pics\\default.jpg"
            filename = "default.jpg"
        else:
            full_profilepic_path = "..\\static\\profile_pics\\" + form.picture.data
            filename = form.picture.data

        # uploading pic
        if 'file' not in request.files:
            flash('No file part')
        else:
            file = request.files['file']

            # if user does not select file, browser also
            # submit a empty part without filename
            if file.filename == '':
                flash('No selected file')
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                #print(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                full_profilepic_path = "..\\static\\profile_pics\\" + filename

        conn = mysql.connect()
        cur = conn.cursor()
        if len(form.password.data) > 0:
            password = form.password.data
            cur.execute("""UPDATE user SET username = %s,password = %s, dob = %s, address = %s, phone = %s, work = %s, education = %s, about = %s, profile_picture = %s WHERE email_id = %s""", (name, password, dob, address, phone, work, education, details, filename, session['logged_user_id']))
            form.password.data = ""
        else:
            cur.execute("""UPDATE user SET username = %s, dob = %s, address = %s, phone = %s, work = %s, education = %s, about = %s, profile_picture = %s WHERE email_id = %s""", (name, dob, address, phone, work, education, details, filename, session['logged_user_id']))
        conn.commit()
        cur.close()
    return render_template('account.html', title='Account', form=form, full_profilepic_path=full_profilepic_path)


def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(account)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))


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

        cur.execute("SELECT * FROM user WHERE email_id = %s and password = %s", (email, password))

        for (emailid) in cur:
            print("{}".format(emailid))
            flag = 1
            user_id = emailid[0]

        cur.close()
        if flag == 0:
            flash('Incorrect username/password.')
        else:
            session['role'] = user_role_id
            session['logged_in'] = True
            session['logged_user_id'] = form.email.data
            session['logged_user_id_num'] = user_id
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
    categories = getCategoryList()
    if session.get('logged_in') is None:
        session['logged_in'] = False

    if session['logged_in'] == True:
        conn = mysql.connect()
        cur = conn.cursor()
        cur.execute('''select * from post inner join user on post.user_id = user.user_id order by post.timestamp desc''')
        result = cur.fetchall()
        view_posts = [list(i) for i in result]
        # print(view_posts)
        if len(view_posts) is 0:
            flash('No posts to display')
        else:
            print('to check if it working')
        return render_template('view.html', view_posts=view_posts,categories=categories)
    else:
        return render_template('index.html', title='View Post',categories=categories)


@app.route('/post', methods=['GET', 'POST'])
def post():
    if session.get('logged_in') is None:
        session['logged_in'] = False

    if session['logged_in'] == True:
        conn = mysql.connect()
        cur = conn.cursor()
        if request.method == 'POST':
            post_id = request.form['id']
            c = request.form['comment']
            cur.execute("INSERT INTO comment(post_id, user_id, comment_text) VALUES(%s, %s, %s)", (post_id, session['logged_user_id_num'], c))
            conn.commit()
        else:
            post_id = request.args.get('id')

        cur.execute('select * from post where post_id = %s', post_id)
        post = cur.fetchone()
        cur.execute('select * from user where user_id = %s', post[1])
        user = cur.fetchone()

        cur.execute('select * from comment where post_id = %s', post_id)
        result = cur.fetchall()
        comments = [list(i) for i in result]
        # Not sure if we need to sort by date, so remove comment if we need to
        # comments = sorted(comments, key=lambda comment: comment[4])
        for i, c in enumerate(comments):
            cur.execute('select * from user where user_id = %s', c[2])
            commentUser = cur.fetchone()
            c.append(commentUser[1])
            comments[i] = c
        return render_template('post.html', post=post, comments=comments, user=(user[0], user[1]))
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

            # timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
            title = form.title.data
            body = form.body.data
            category = request.form["category"]
            user_email = session['logged_user_id']

            conn = mysql.connect()
            cur = conn.cursor()
            cur.execute("SELECT * FROM user WHERE email_id = %s", (user_email))
            for (user) in cur:
                user_id = str(user[0])

            cur.execute("INSERT INTO post(category_id, post_text, post_title, user_id) VALUES(%s, %s, %s, %s)", (category, body, title, user_id))
            id = cur.lastrowid
            conn.commit()

            return redirect('/post?id=' + str(id))

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
    categories = getCategoryList()
    if request.method == "POST":
        conn = mysql.connect()
        cur = conn.cursor()
        
        search_text = request.form['search']
        filter_type = request.form['filter_by']
        category = request.form['category']
        less_date = request.form['less_date']
        great_date = request.form['great_date']
        
        
        where_string = ""
        if len(search_text)>0 :
            if filter_type == 'text':
                where_string = where_string + " post_title like '%" +search_text + "%' and"
            
            if filter_type == 'user':
                where_string = where_string + " post.user_id IN (SELECT user_id from user where username like '%"+search_text+"%') and"
        
        if category!='0' :
            where_string = where_string + " category_id = " +category + " and"
        
        if len(less_date)>0 :
            where_string = where_string + " post.timestamp <= '"+less_date+"' and"
        
        if len(great_date)>0 :
            where_string = where_string + " post.timestamp >= '"+great_date+"' and"
        
        
        where_string = where_string[:-3]
        
        if len(where_string)>0:
            where_string = "where " + where_string 
        
        
        cur.execute('''SELECT * from post inner join user on post.user_id = user.user_id '''+ where_string + '''''')

        result = cur.fetchall()
        searched_posts = [list(i) for i in result]
        # print(searched_posts)
        if len(searched_posts) is 0:
            flash('No results Found!')
        else:
            print
        return render_template('search.html', searched_posts=searched_posts, categories=categories)  # <- Here you jump away from whatever result you create
   # return render_template('view.html')


@app.route('/list_admin', methods=['GET', 'POST'])
def list_admin():
    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute('''SELECT * from user where user_role = 2''')
    result = cur.fetchall()
    admins_list = [list(i) for i in result]

    return render_template('list_admin.html', admins_list=admins_list)  # <- Here you jump away from whatever result you create
   # return render_template('view.html')

# route for User Profile


# @app.route("/account", methods=['POST'])
# def account():
#     form = UpdateAccountForm(request.form)
#     if request.method == 'POST' and form.validate():
#         name = form.name.data
#         email = form.email.data
#         dob = form.dob.data
#         address = form.address.data
#         phone = form.phone.data
#         work = form.work.data
#         education = form.education.data
#         details = form.details.data

#         conn = mysql.connect()
#         cur = conn.cursor()
#         cur.execute(
#             "INSERT INTO user(username, email_id, dob, address, phone, work, education, details)"
#             " VALUES(%s, %s, %s, %s, %s, %s)",
#             (name, email, dob, address, phone, work, education, details))
#         conn.commit()
#         cur.close()
#     return render_template('account.html', title='Account', form=form)


#form = UpdateAccountForm()
# return render_template('account.html', title='Account')


# def validate_email(self, email):
#     if email.data != current_user.email:
#         user = User.query.filter_by(email=email.data).first()
#         if user:
#             raise ValidationError('That email is taken. Please choose a different one.')

def getCategoryList():
    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM category")
    result = cur.fetchall()
    category_list = [list(i) for i in result]

    return category_list


# def save_picture(form_picture):
#     random_hex = secrets.token_hex(8)
#     _, f_ext = os.path.splitext(form_picture.filename)
#     picture_fn = random_hex + f_ext
#     picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

#     output_size = (125, 125)
#     i = Image.open(form_picture)
#     i.thumbnail(output_size)
#     i.save(picture_path)

#     return picture_fn


if __name__ == '__main__':

    app.run(debug=True, host='0.0.0.0')
