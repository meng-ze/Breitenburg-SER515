from ConstantTable import ErrorCode, DatabaseModel, AccountInfo, AccountRoleInfo, PostInfo, CommentInfo, BlockInfo
import os

def is_user_exist(email, website):
    connection_handler = website.mysql_server.connect()
    cursor = connection_handler.cursor()
    cursor.execute("SELECT * FROM user WHERE {} = %s".format(AccountInfo.EMAIL), (email))
    number_of_rows = len(cursor.fetchall())
    cursor.close()

    if number_of_rows != 0:
        return True
    return False

def verify_login_password(email, password, website):
    if is_user_blocked(email, website):
        return (False, {ErrorCode.ERROR_CODE: ErrorCode.USER_IS_BLOCKED})
    try:
        connection_handler = website.mysql_server.connect()
        cursor = connection_handler.cursor()
        cursor.execute("SELECT * FROM user inner join user_role on user.user_role = user_role.id WHERE email_id = %s and password = %s", (email, password))
        for content in cursor:
            cursor.close()
            content_dict = {
                AccountInfo.EMAIL: email,
                AccountInfo.USER_ID: content[0],
                AccountInfo.USER_ROLE_ID: content[10]
            }
            return (True, content_dict)
        
    except Exception as e:
        print('Error!')
        print(e)

    if cursor != None:
        cursor.close()
    return (False, {ErrorCode.ERROR_CODE: ErrorCode.PASSWORD_INCORRECT})

def create_account(username: str, other_info: {str: None}, website):
    cursor = None
    try:
        connection_handler = website.mysql_server.connect()
        cursor = connection_handler.cursor()
        if AccountInfo.USER_ROLE_ID in other_info:
            cursor.execute('INSERT INTO {}({}, {}, {}, {}, {}, {}, {}) VALUES(%s, %s, %s, %s, %s, %s, %s);'.format(DatabaseModel.USER,
                AccountInfo.USERNAME, AccountInfo.EMAIL, AccountInfo.USER_ROLE_ID, AccountInfo.PASSWORD,
                AccountInfo.PHONE, AccountInfo.DATE_OF_BIRTH, AccountInfo.GENDER),(

                username, other_info[AccountInfo.EMAIL], other_info[AccountInfo.USER_ROLE_ID], other_info[AccountInfo.PASSWORD],
                other_info[AccountInfo.PHONE], other_info[AccountInfo.DATE_OF_BIRTH], other_info[AccountInfo.GENDER])
                )
        else:
            cursor.execute('INSERT INTO {}({}, {}, {}, {}, {}, {}) VALUES(%s, %s, %s, %s, %s, %s);'.format(DatabaseModel.USER,
                AccountInfo.USERNAME, AccountInfo.EMAIL, AccountInfo.PASSWORD,
                AccountInfo.PHONE, AccountInfo.DATE_OF_BIRTH, AccountInfo.GENDER),(

                username, other_info[AccountInfo.EMAIL], other_info[AccountInfo.PASSWORD],
                other_info[AccountInfo.PHONE], other_info[AccountInfo.DATE_OF_BIRTH], other_info[AccountInfo.GENDER])
                )
        connection_handler.commit()
        cursor.close()

        return True

    except Exception as e:
        print('Error!')
        print(e)

    if cursor != None:
        cursor.close()
    return False


# def modify_account(username: str, key: str, value: None)
# def delete_account(username: str)
# def get_account_info(username: str) -> {str: None}

# ---
""" Actions below MUST include timestamp """
def modify_account(target_email, value_dict, website):
    cursor = None
    try:
        connection_handler = website.mysql_server.connect()
        cursor = connection_handler.cursor()
        if AccountInfo.PASSWORD in value_dict:
            cursor.execute(
                'UPDATE user SET username = %s, password = %s, dob = %s, address = %s, phone = %s, work = %s, education = %s, about = %s, profile_picture = %s WHERE email_id = %s',
                (value_dict[AccountInfo.USERNAME], value_dict[AccountInfo.PASSWORD], value_dict[AccountInfo.DATE_OF_BIRTH], value_dict[AccountInfo.ADDRESS],
                 value_dict[AccountInfo.PHONE], value_dict[AccountInfo.WORK], value_dict[AccountInfo.EDUCATION], value_dict[AccountInfo.ABOUT],
                 value_dict[AccountInfo.PROFILE_PICTURE], target_email)
                )
        else:
            cursor.execute(
                'UPDATE user SET username = %s, dob = %s, address = %s, phone = %s, work = %s, education = %s, about = %s, profile_picture = %s WHERE email_id = %s',
                (value_dict[AccountInfo.USERNAME], value_dict[AccountInfo.DATE_OF_BIRTH], value_dict[AccountInfo.ADDRESS],
                 value_dict[AccountInfo.PHONE], value_dict[AccountInfo.WORK], value_dict[AccountInfo.EDUCATION], value_dict[AccountInfo.ABOUT],
                 value_dict[AccountInfo.PROFILE_PICTURE], target_email)
                )        
        connection_handler.commit()
        cursor.close()

        return True
    except Exception as e:
        print('Error!')
        print(e)

    if cursor != None:
        cursor.close()
    return False

def create_post(email, title, body, category, website):
    """
    Create a post for username 
    This function will create a post for 'username' and insert this post into our database.
    """
    cursor = None
    try:
        connection_handler = website.mysql_server.connect()
        cursor = connection_handler.cursor()
        cursor.execute('SELECT * FROM {} WHERE {} = "{}"'.format(DatabaseModel.USER, AccountInfo.EMAIL, email))
        for user in cursor:
            user_id = str(user[0])

        cursor.execute('INSERT INTO {}({}, {}, {}, {}) VALUES(%s, %s, %s, %s);'.format(DatabaseModel.POST,
            PostInfo.CATEGORY_ID, PostInfo.POST_TEXT, PostInfo.POST_TITLE, PostInfo.USER_ID), 
            (category, body, title, user_id))
        post_id = cursor.lastrowid
        connection_handler.commit()
        cursor.close()

        return (True, post_id)
    except Exception as e:
        print('Error!')
        print(e)

    if cursor != None:
        cursor.close()
    return (False, None)

def create_comment(post_id, user_id, comment_content, website):
    cursor = None
    try:
        connection_handler = website.mysql_server.connect()
        cursor = connection_handler.cursor()
        cursor.execute('INSERT INTO {}({}, {}, {}) VALUES(%s, %s, %s)'.format(DatabaseModel.COMMENT, 
        PostInfo.POST_ID, PostInfo.USER_ID, CommentInfo.COMMENT_TEXT), (post_id, user_id, comment_content))
        connection_handler.commit()
        cursor.close()

        return True
    except Exception as e:
        print('Error!')
        print(e)

    if cursor != None:
        cursor.close()
    return False

def get_category_list(website):
    connection_handler = website.mysql_server.connect()
    cursor = connection_handler.cursor()
    cursor.execute("SELECT * FROM {}".format(DatabaseModel.CATEGORY))
    result = cursor.fetchall()
    category_list = [list(i) for i in result]
    
    return category_list

def get_all_posts(website, inner_join=True, order=None, filter_dict=None):
    """
    Query database for list(post_id)
    If the our database does NOT exist post_id, return False and return function, print("Error: ERROR_CODE[2]) -> False
    """
    cursor = None
    try:
        connection_handler = website.mysql_server.connect()
        cursor = connection_handler.cursor()

        fetch_all_posts_command = 'SELECT * FROM {}'.format(DatabaseModel.POST)

        inner_join_command = ''
        if inner_join:
            inner_join_command = 'INNER JOIN {1} ON {0}.{2} = {1}.{3}'.format(DatabaseModel.POST, DatabaseModel.USER, PostInfo.USER_ID, AccountInfo.USER_ID)

        order_command = ''
        if order != None:
            order_command = 'ORDER BY {} DESC'.format(order)

        filter_command = ''
        if filter_dict != None:
            decompose_arr = []
            for key in filter_dict:
                individual_query = '{} {}'.format(key, filter_dict[key])
                decompose_arr.append(individual_query)
            filter_str = 'WHERE ' + ' AND '.join(decompose_arr)
            filter_command = filter_str

        query_command = ' '.join([fetch_all_posts_command, inner_join_command, order_command, filter_command])
        print(query_command)
        cursor.execute(query_command)
        posts = cursor.fetchall()
        posts = [list(post) for post in posts]

        return posts

    except Exception as e:
        print('Error!')
        print(e)
    if cursor != None:
        cursor.close()
    return []

def get_all_comments(post_id, website, filter_dict=None):
    cursor = None
    try:
        connection_handler = website.mysql_server.connect()
        cursor = connection_handler.cursor()
        fetch_all_comments_command = 'SELECT * FROM {}'.format(DatabaseModel.COMMENT)
        
        filter_command = ''
        if filter_dict != None:
            decompose_arr = []
            for key in filter_dict:
                individual_query = '{} = "{}"'.format(key, filter_dict[key])
                decompose_arr.append(individual_query)
            filter_str = 'WHERE ' + 'AND'.join(decompose_arr)
            filter_command = filter_str

        query_command = ' '.join([fetch_all_comments_command, filter_command])
        cursor.execute(query_command)
        comments = cursor.fetchall()
        comments = [list(comment) for comment in comments]

        return comments

    except Exception as e:
        print('Error!')
        print(e)
    if cursor != None:
        cursor.close()
    return []

def get_user_info(filter_dict, website, list_mode=False):
    cursor = None
    try:
        connection_handler = website.mysql_server.connect()
        cursor = connection_handler.cursor()

        for key in filter_dict:
            cursor.execute('SELECT * FROM {} WHERE {} = %s'.format(DatabaseModel.USER, key), (filter_dict[key]))
        if list_mode == False:
            user_info = cursor.fetchone()
        else:
            user_info = cursor.fetchall()

        cursor.close()
        return user_info

    except Exception as e:
        print('Error!')
        print(e)
    if cursor != None:
        cursor.close()
    return None

def delete(datamodel_type, filter_dict, website):
    cursor = None
    try:
        connection_handler = website.mysql_server.connect()
        cursor = connection_handler.cursor()

        for key in filter_dict:
            cursor.execute("DELETE FROM {} WHERE {} = %s".format(datamodel_type, key), (filter_dict[key]))
        connection_handler.commit()
        cursor.close()
        return True
        
    except Exception as e:
        print('Error!')
        print(e)
    if cursor != None:
        cursor.close()
    return False

def is_user_blocked(email, website):
    connection_handler = website.mysql_server.connect()
    cursor = connection_handler.cursor()
    cursor.execute("SELECT * FROM {} WHERE {} = %s".format(DatabaseModel.BLOCK_USER, BlockInfo.EMAIL), (email))
    number_of_rows = len(cursor.fetchall())
    cursor.close()

    if number_of_rows != 0:
        return True
    return False

def block_user(email, website):
    cursor = None
    if is_user_blocked(email, website):
        return (False, ErrorCode.USER_IS_BLOCKED)
    if is_user_exist(email, website) == False:
        return (False, ErrorCode.USER_NOT_EXIST)

    try:
        connection_handler = website.mysql_server.connect()
        cursor = connection_handler.cursor()
        cursor.execute('INSERT INTO {}({}) VALUES(%s);'.format(DatabaseModel.BLOCK_USER, BlockInfo.EMAIL), (email))
        connection_handler.commit()
        cursor.close()
        return (True, ErrorCode.SUCCESS)
    except Exception as e:
        print('Error!')
        print(e)

    if cursor != None:
        cursor.close()

    return (False, None)

def get_all_blocked_users(website):
    cursor = None
    try:
        connection_handler = website.mysql_server.connect()
        cursor = connection_handler.cursor()
        cursor.execute('SELECT * FROM {}'.format(DatabaseModel.BLOCK_USER))
        blocked_email_list = cursor.fetchall()

        return blocked_email_list

    except Exception as e:
        print('Error!')
        print(e)

    if cursor != None:
        cursor.close()
    return []

def extract_profile_data_from(user_info):
    return_data = [
        user_info[1],
        user_info[2],
        user_info[6],
        user_info[9],
        user_info[4],
        user_info[10],
        user_info[11],
        user_info[12],
        user_info[13],
    ]
    return return_data

def get_relative_path(relative_formatted_path):
    relative_level = relative_formatted_path[0]
    target_path = relative_formatted_path[1]
    while relative_level != 0:
        target_path.insert(0, '..')
        relative_level += 1
    return os.path.join(*target_path)

def is_allowed_file(filename, website):
    basename = os.path.basename(filename)
    file_extension = os.path.splitext(basename)[-1].replace('.', '')
    file_extension = file_extension.lower()
    if file_extension in website.allowed_file_type:
        return True
    return False
    

# def get_comments([comment_id: address]) -> list(Post):
#     """
#     Query database for list(comment_id)
#     If the our database does NOT exist comment_id, return False and return function, print("Error: ERROR_CODE[2]) -> False
#     """
# def query_by_keyword(keyword) -> list(Post):
#     """
#     Query 'Post' database using keyword
#     """
# def query_by_username(username) -> list(Post):
#     """
#     Query 'Post' database using keyword
#     """
# def query_by_date_range(start_date, end_date) -> list(Post):
#     """
#     Query 'Post' database from 'start_date' to 'end_date'
#     """

# non-deterministic yet
#def upload_file(filepath: str, media_type: str, attached_post: Post)


# def modify_post(username: Account, post_id: address, description: str) -> bool:
#     """
#     This will first call 'get_posts(post_id)', if it return False -> False
#     If the post_id does exist in our database, but the user of that post does not have permission (corresponding to current user), print "Error: ERROR_CODE[1]" -> False
#     If the post_id does exist in our database, and current does have permission to modify this post, then REPLACE the old keyvalue in database with description -> True 
#     """
# def delete_post(username: Account, post_id: address):
#     """
#     This will first call 'get_posts(post_id)', if it return False -> False
#     If the post_id does exist in our database, but the user of that post does not have permission (corresponding to current user), print "Error: ERROR_CODE[1]" -> False
#     If the post_id does exist in our database, and current does have permission to modify this post, then DELETE the Post(post_id) in database, return success -> True
#     """
# def delete_comment(username: Account, comment_id: address, description: str):
#     """
#     This will first call 'get_comments(comment_id)', if it return False -> False
#     If the comment_id does exist in our database, but the user of that post does not have permission (corresponding to current user), print("Error: ERROR_CODE[1]") -> False
#     If the comment_id does exist in our database, and current does have permission to modify this post, then DELETE the Post(post_id) in database, return success -> True
#     """