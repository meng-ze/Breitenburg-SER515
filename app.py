from flask import Flask, render_template, redirect, url_for, request, flash, session
#from data import Articles
from Website import Website
from flaskext.mysql import MySQL
import CustomForm
import WebsiteAPI
from ConstantTable import ErrorCode, DatabaseModel, AccountInfo, PostInfo, CommentInfo, WebsiteLoginStatus, DefaultFileInfo, RoleType
from werkzeug.utils import secure_filename
import time
import datetime

app = Flask(__name__)
mysql_server = MySQL()
main_website = Website(app, mysql_server)


@app.route('/')
def index():
    if session.get(WebsiteLoginStatus.LOGGED_IN) is None:
        session[WebsiteLoginStatus.LOGGED_IN] = False

    category = None
    if 'category' in request.args:
        category = request.args['category']

    all_posts = WebsiteAPI.get_all_posts(main_website, order = True, post_category = category)
    if len(all_posts) == 0:
        flash('No posts to display')

    lst = list(all_posts)
    new_lst = list()
    for element in lst:
        my_email_id = element[8]
        my_user_info = WebsiteAPI.get_user_info({AccountInfo.EMAIL: my_email_id}, main_website)
        required_info = WebsiteAPI.extract_profile_data_from(my_user_info)
        if required_info[-1]:
            full_profilepic_path = WebsiteAPI.get_relative_path(
                [-1, [DefaultFileInfo.AVATAR_PATH[1][0], DefaultFileInfo.AVATAR_PATH[1][1], required_info[-1]]])
        else:
            full_profilepic_path = WebsiteAPI.get_relative_path(DefaultFileInfo.AVATAR_PATH)
        element = element + (full_profilepic_path,)
        print(element)
        new_lst.append(element)

    return render_template('index.html', view_posts=new_lst)


# Data Analystics
@app.route('/analysis', methods=['GET', 'POST'])
def analysis():
    # print("here")
    results1 = WebsiteAPI.getDataForBarGraph(main_website)
    # print(results1)
    months = []
    years = []
    no_of_posts = []

    for i in results1:
        months.append(i[0])
        years.append(i[1])
        no_of_posts.append(i[2])

    labels = months
    values = no_of_posts

    results5 = WebsiteAPI.get_typeof_users(main_website)
    # print(results5)

    typeof_users = []
    noof_users = []

    for i in results5:
        typeof_users.append(i[0])
        noof_users.append(i[1])

    # typeof_users.append('MAd people')
    # print(typeof_users)
    # print(noof_users)

    labels_pie = typeof_users
    values_pie = noof_users
    colors_pie = ["#F34353", "#F38630", "#FEDCBA", "#46BFBD", "#FDB45C", "#ABCDEF", "#DDDDDD", "#ABCABC"]

    if len(labels_pie) == 2:
        colors = ["Red", "Orange"]
    else:
        colors = ["Red", "Orange", "Pink"]
    dict1 = dict(zip(typeof_users, colors))
    # print(dict1)
    results2 = WebsiteAPI.getDataForLineGraph(main_website)
    # print(results)
    category = []
    noOfPosts = []

    for i in results2:
        category.append(i[0])
        noOfPosts.append(i[1])

    labels2 = category
    values2 = noOfPosts

    results3 = WebsiteAPI.get_registered_users(main_website)
    # print(registered_users)

    registered_users = []
    for i in results3:
        registered_users.append(i[0])

    results4 = WebsiteAPI.get_total_posts(main_website)
    # print(registered_users)

    no_of_posts = []
    for i in results4:
        no_of_posts.append(i[0])

    return render_template('analysis.html', values=values, labels=labels, values2=values2, labels2=labels2, set=zip(values_pie, labels_pie, colors_pie), results1=results1, results2=results2, registered_users=registered_users, no_of_posts=no_of_posts, dict1=dict1)


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
                AccountInfo.GENDER: 'M',
                AccountInfo.PROFILE_PICTURE: DefaultFileInfo.AVATAR_FILE_NAME
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
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = CustomForm.LoginForm(request.form, main_website)
    if request.method == 'POST' and form.validate():
        email = form.email_field.data
        password = form.password_field.data

        login_success = WebsiteAPI.verify_login_password(email, password, main_website)
        if not login_success[0]:
            if login_success[1][ErrorCode.ERROR_CODE] == ErrorCode.USER_IS_BLOCKED:
                flash('Your account has been blocked!')
            elif login_success[1][ErrorCode.ERROR_CODE] == ErrorCode.PASSWORD_INCORRECT:
                flash('Incorrect username/password.')
        else:
            session[WebsiteLoginStatus.LOGGED_IN] = True
            session[WebsiteLoginStatus.LOGGED_USER_EMAIL] = login_success[1][AccountInfo.EMAIL]
            session[WebsiteLoginStatus.LOGGED_USER_ID] = login_success[1][AccountInfo.USER_ID]
            session[WebsiteLoginStatus.LOGGED_USER_ROLE_ID] = login_success[1][AccountInfo.USER_ROLE_ID]
            flash('You were successfully logged in')
            return redirect(url_for('view'))
    return render_template('login.html', title='Login', form=form)


@app.route('/name_click', methods=['GET', 'POST'])
def name_click():
    if request.method == 'GET':
        if session.get(WebsiteLoginStatus.LOGGED_IN) is None:
            session[WebsiteLoginStatus.LOGGED_IN] = False

        if session[WebsiteLoginStatus.LOGGED_IN] == True:
            chosen_user_email = request.args['user']
            chosen_user_info = WebsiteAPI.get_user_info({AccountInfo.EMAIL: chosen_user_email}, main_website)
            required_info = WebsiteAPI.extract_profile_data_from(chosen_user_info)

            if required_info[-1]:
                full_profilepic_path = WebsiteAPI.get_relative_path([-1, ['static', 'profile_pics', required_info[-1]]])
            else:
                full_profilepic_path = WebsiteAPI.get_relative_path(DefaultFileInfo.AVATAR_PATH)
            return render_template('ViewProfile.html', title='Profile', posts=[required_info], full_profilepic_path=full_profilepic_path)
        else:
            return render_template('index.html', title='Home')


@app.route('/account', methods=['GET', 'POST'])
def account():
    form = CustomForm.UpdateAccountForm(request.form)
    if request.method == 'GET':
        if session.get(WebsiteLoginStatus.LOGGED_IN) is None:
            session[WebsiteLoginStatus.LOGGED_IN] = False

        if session[WebsiteLoginStatus.LOGGED_IN] == True:
            my_email_id = session[WebsiteLoginStatus.LOGGED_USER_EMAIL]
            my_user_info = WebsiteAPI.get_user_info({AccountInfo.EMAIL: my_email_id}, main_website)
            required_info = WebsiteAPI.extract_profile_data_from(my_user_info)

            form.name_field.data = required_info[0]
            form.email_field.data = required_info[1]
            form.dob_field.data = required_info[2]
            form.address_field.data = required_info[3]
            form.phone_field.data = required_info[4]
            form.work_field.data = required_info[5]
            form.education_field.data = required_info[6]
            form.details_field.data = required_info[7]
            form.picture_field.data = required_info[8]
            if required_info[-1]:
                full_profilepic_path = WebsiteAPI.get_relative_path([-1, [DefaultFileInfo.AVATAR_PATH[1][0], DefaultFileInfo.AVATAR_PATH[1][1], required_info[-1]]])
            else:
                full_profilepic_path = WebsiteAPI.get_relative_path(DefaultFileInfo.AVATAR_PATH)

            return render_template('account.html', title='My Profile', form=form, full_profilepic_path=full_profilepic_path)
        else:
            return render_template('index.html', title='Home')

    if request.method == 'POST':
        name = form.name_field.data
        dob = form.dob_field.data
        address = form.address_field.data
        phone = form.phone_field.data
        work = form.work_field.data
        education = form.education_field.data
        details = form.details_field.data

        my_email_id = session[WebsiteLoginStatus.LOGGED_USER_EMAIL]
        my_profile_file_name = WebsiteAPI.get_user_info({AccountInfo.EMAIL: my_email_id}, main_website)[-1]
        form.picture_field.data = my_profile_file_name
        if not form.picture_field.data:
            full_profilepic_path = WebsiteAPI.get_relative_path(DefaultFileInfo.AVATAR_PATH)
            filename = DefaultFileInfo.AVATAR_PATH[-1][-1]
        else:
            full_profilepic_path = WebsiteAPI.get_relative_path([-1, [DefaultFileInfo.AVATAR_PATH[1][0], DefaultFileInfo.AVATAR_PATH[1][1], form.picture_field.data]])
            filename = form.picture_field.data

        packed_dict = {
            AccountInfo.USERNAME: name,
            AccountInfo.DATE_OF_BIRTH: dob,
            AccountInfo.ADDRESS: address,
            AccountInfo.PHONE: phone,
            AccountInfo.WORK: work,
            AccountInfo.EDUCATION: education,
            AccountInfo.ABOUT: details,
            AccountInfo.PROFILE_PICTURE: my_profile_file_name
        }

        # uploading pic
        if 'file' not in request.files:
            flash('No file part')
            relative_profilepic_path = full_profilepic_path
        else:
            chosen_file = request.files['file']

            if chosen_file.filename == '':
                flash('No selected file')
            if chosen_file and WebsiteAPI.is_allowed_file(chosen_file.filename, main_website):
                filename = secure_filename(chosen_file.filename)
                full_profilepic_path = WebsiteAPI.get_relative_path([0, [main_website.upload_folder, filename]])
                relative_profilepic_path = WebsiteAPI.get_relative_path([-1, [DefaultFileInfo.AVATAR_PATH[1][0], DefaultFileInfo.AVATAR_PATH[1][1], filename]])
                chosen_file.save(full_profilepic_path)
                chosen_file.close()

                packed_dict[AccountInfo.PROFILE_PICTURE] = filename

        if len(form.password_field.data) > 0:
            packed_dict[AccountInfo.PASSWORD] = form.password_field.data

        WebsiteAPI.modify_account(my_email_id, packed_dict, main_website)

        form.password_field.data = ""
    return render_template('account.html', title='Account', form=form, full_profilepic_path=relative_profilepic_path)


@app.route('/view')
def view():
    if session.get(WebsiteLoginStatus.LOGGED_IN) is None:
        session[WebsiteLoginStatus.LOGGED_IN] = False

    if session[WebsiteLoginStatus.LOGGED_IN] == True:

        category = None
        if 'category' in request.args:
            category = request.args['category']


        all_posts = WebsiteAPI.get_all_posts(main_website, order='{}.{}'.format(DatabaseModel.POST, PostInfo.TIMESTAMP), post_category = category)
        if len(all_posts) == 0:
            flash('No posts to display')

        lst = list(all_posts)
        new_lst = list()
        for element in lst:
            my_email_id = element[8]
            my_user_info = WebsiteAPI.get_user_info({AccountInfo.EMAIL: my_email_id}, main_website)
            required_info = WebsiteAPI.extract_profile_data_from(my_user_info)
            if required_info[-1]:
                full_profilepic_path = WebsiteAPI.get_relative_path(
                    [-1, [DefaultFileInfo.AVATAR_PATH[1][0], DefaultFileInfo.AVATAR_PATH[1][1], required_info[-1]]])
            else:
                full_profilepic_path = WebsiteAPI.get_relative_path(DefaultFileInfo.AVATAR_PATH)
            element = element + (full_profilepic_path,)
            print(element)
            new_lst.append(element)

        return render_template('view.html', view_posts=new_lst)
    else:
        return render_template('index.html', title='View Post')


@app.route('/search', methods=['GET', 'POST'])
def search():
    categories = WebsiteAPI.get_category_list(main_website)
    if request.method == "POST":

        search_text = request.form['search']
        filter_type = request.form['filter_by']
        category = request.form['category']
        less_date = request.form['less_date']
        great_date = request.form['great_date']

        filter_dict = {}
        if len(search_text) > 0:
            if filter_type == 'text':
                filter_dict[PostInfo.POST_TITLE] = ' like \'%' + search_text + '%\''

            if filter_type == 'user':
                filter_dict['{}.{}'.format(DatabaseModel.POST, PostInfo.USER_ID)] = ' IN (SELECT user_id from user where username like \'%' + search_text + '%\')'

        if category != '0':
            filter_dict[PostInfo.CATEGORY_ID] = ' = ' + category

        if len(less_date) > 0:
            filter_dict['{}.{} <= '.format(DatabaseModel.POST, PostInfo.TIMESTAMP)] = less_date

        if len(great_date) > 0:
            filter_dict['{}.{} >= '.format(DatabaseModel.POST, PostInfo.TIMESTAMP)] = great_date

        all_posts = WebsiteAPI.get_all_posts(main_website, inner_join=True, filter_dict=filter_dict)

        # print(searched_posts)
        if len(all_posts) is 0:
            flash('No results Found!')
        return render_template('search.html', searched_posts=all_posts, categories=categories)  # <- Here you jump away from whatever result you create
   # return render_template('view.html')


@app.route('/my_posts', methods=['GET', 'POST'])
def my_posts():
    if session.get(WebsiteLoginStatus.LOGGED_IN) is None:
        session[WebsiteLoginStatus.LOGGED_IN] = False

    if session[WebsiteLoginStatus.LOGGED_IN] == True:
        logged_user_id = session[WebsiteLoginStatus.LOGGED_USER_ID]
        all_posts = WebsiteAPI.get_all_posts(main_website, inner_join=False, filter_dict={AccountInfo.USER_ID: ' = {}'.format(logged_user_id)})

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
            post = WebsiteAPI.get_all_posts(main_website, False, filter_dict={PostInfo.POST_ID: ' = {}'.format(post_id)})

        return render_template('edit_post.html', title='Edit Post', post=post)
    else:
        return render_template('index.html', title='Home')


@app.route('/post', methods=['GET', 'POST'])
def post():
    if session.get(WebsiteLoginStatus.LOGGED_IN) is None:
        session[WebsiteLoginStatus.LOGGED_IN] = False

    if session[WebsiteLoginStatus.LOGGED_IN] == True:
        if request.method == 'POST':
            post_id = request.form['id']
            comment_content = request.form['comment']
            print('All comments:\n', WebsiteAPI.get_all_comments(post_id, main_website, filter_dict={PostInfo.POST_ID: post_id}))
            print('---------------')
            WebsiteAPI.create_comment(post_id, session[WebsiteLoginStatus.LOGGED_USER_ID], comment_content, main_website)
        else:
            post_id = request.args.get('id')
            print('post_id:', post_id)

        chosen_post = WebsiteAPI.get_all_posts(main_website, inner_join=False, filter_dict={PostInfo.POST_ID: ' = {}'.format(post_id)})[0]
        print('Chosen_post: ', chosen_post)
        user_id_of_chosen_post = chosen_post[1]
        user_info = WebsiteAPI.get_user_info({AccountInfo.USER_ID: user_id_of_chosen_post}, main_website)
        is_admin = session[WebsiteLoginStatus.LOGGED_USER_ROLE_ID] == RoleType.ADMIN
        is_post_owner = user_id_of_chosen_post == session[WebsiteLoginStatus.LOGGED_USER_ID]
        is_admin_of_this_post = is_admin or is_post_owner

        comments = WebsiteAPI.get_all_comments(post_id, main_website, filter_dict={PostInfo.POST_ID: post_id})

        for idx in range(len(comments)):
            comment = comments[idx]
            comment_user = WebsiteAPI.get_user_info({AccountInfo.USER_ID: comment[2]}, main_website)
            comment.append(comment_user[1])
            comments[idx] = comment
        return render_template('post.html', post=chosen_post, comments=comments, user=(user_info[0], user_info[1]), admin=is_admin_of_this_post)
    else:
        return render_template('index.html', title='Post')


@app.route('/admin_delete_post', methods=['POST'])
def admin_delete_post():
    post_id = request.form['post_id']
    comment_id = request.form['comment_id']

    view_id = request.form['view_id']
    post_user_id = WebsiteAPI.get_all_posts(main_website, inner_join=False, filter_dict={PostInfo.POST_ID: ' = {}'.format(view_id)})[0][1]

    my_user_info = WebsiteAPI.get_user_info({AccountInfo.EMAIL: session[WebsiteLoginStatus.LOGGED_USER_EMAIL]}, main_website)

    am_i_admin = session[WebsiteLoginStatus.LOGGED_USER_ROLE_ID] == RoleType.ADMIN
    if not am_i_admin and my_user_info[0] != post_user_id:  # If the current user's role is not admin
        flash('Unauthorized!')
        return redirect(url_for('view'))  # Redirect back to the main page

    if int(comment_id) == -1:
        WebsiteAPI.delete(DatabaseModel.POST, {PostInfo.POST_ID: post_id}, main_website)
        WebsiteAPI.delete(DatabaseModel.COMMENT, {PostInfo.POST_ID: post_id}, main_website)
    elif int(post_id) == -1:
        WebsiteAPI.delete(DatabaseModel.COMMENT, {CommentInfo.COMMENT_ID: comment_id}, main_website)
        return redirect("/post?id=" + str(view_id))

    return redirect(url_for('view'))


@app.route('/createPost', methods=['GET', 'POST'])
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

# Admin feature


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


@app.route('/block_user', methods=['GET', 'POST'])
def block_user():
    form = CustomForm.BlockUserForm(request.form)
    if request.method == 'POST' and form.validate():
        email = form.email_field.data
        block_success = WebsiteAPI.block_user(email, main_website)
        if not block_success[0]:
            if block_success[1] == ErrorCode.USER_IS_BLOCKED:
                flash('User has already been blocked')
            elif block_success[1] == ErrorCode.USER_NOT_EXIST:
                flash('User does not exist!')
        else:
            return redirect(url_for('block_user'))

    blocked_email_list = WebsiteAPI.get_all_blocked_users(main_website)
    blocked_user_info_list = []
    for email in blocked_email_list:
        user_info = WebsiteAPI.get_user_info({AccountInfo.EMAIL: email}, main_website)
        blocked_user_info_list.append(user_info)

    return render_template('block_user.html', title='Block Users', form=form, block_list=blocked_user_info_list)


@app.route('/list_admin', methods=['GET', 'POST'])
def list_admin():
    admins_list = WebsiteAPI.get_user_info({AccountInfo.USER_ROLE_ID: 2}, main_website, list_mode=True)
    return render_template('list_admin.html', admins_list=admins_list)  # <- Here you jump away from whatever result you create

class DebugableApp():
    def __init__(self):
        self.website = main_website

if __name__ == '__main__':
    debugable_app = DebugableApp()
    debugable_app.website.app.run(debug=True, host='0.0.0.0')
