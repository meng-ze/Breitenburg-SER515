from ConstantTable import DatabaseModel, AccountInfo, AccountRoleInfo, PostInfo

def is_user_exist(email, website):
    connection_handler = website.mysql_server.connect()
    cursor = connection_handler.cursor()
    number_of_rows = cursor.execute("SELECT * FROM user WHERE email_id = %s", (email))
    cursor.close()

    if number_of_rows == 0:
        return True
    return False


def verify_login_password(email, password, website):
    try:
        connection_handler = website.mysql_server.connect()
        cursor = connection_handler.cursor()
        cursor.execute('SELECT * FROM {0} INNER JOIN {0}.{1} = "{1}.{2}" WHERE {3} = "{4}" and {5} = "{6}"'.format(DatabaseModel.USER,
            DatabaseModel.USER_ROLE, AccountRoleInfo.ID, AccountInfo.EMAIL, email, AccountInfo.PASSWORD, password)
        )
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
    return (False, None)

def create_account(username: str, other_info: {str: None}, website):
    cursor = None
    try:
        connection_handler = website.mysql_server.connect()
        cursor = connection_handler.cursor()
        if AccountInfo.USER_ROLE_ID in other_info:
            create_user_command = 'INSERT INTO {}({}, {}, {}, {}, {}, {}, {}) VALUES("{}", "{}", "{}", "{}", "{}", "{}", "{}");'.format(DatabaseModel.USER,
                AccountInfo.USERNAME, AccountInfo.EMAIL, AccountInfo.USER_ROLE_ID, AccountInfo.PASSWORD,
                AccountInfo.PHONE, AccountInfo.DATE_OF_BIRTH, AccountInfo.GENDER,

                username, other_info[AccountInfo.EMAIL], other_info[AccountInfo.USER_ROLE_ID], other_info[AccountInfo.PASSWORD],
                other_info[AccountInfo.PHONE], other_info[AccountInfo.DATE_OF_BIRTH], other_info[AccountInfo.GENDER]
                )
        else:
            create_user_command = 'INSERT INTO {}({}, {}, {}, {}, {}, {}) VALUES("{}", "{}", "{}", "{}", "{}", "{}");'.format(DatabaseModel.USER,
                AccountInfo.USERNAME, AccountInfo.EMAIL, AccountInfo.PASSWORD,
                AccountInfo.PHONE, AccountInfo.DATE_OF_BIRTH, AccountInfo.GENDER,

                username, other_info[AccountInfo.EMAIL], other_info[AccountInfo.PASSWORD],
                other_info[AccountInfo.PHONE], other_info[AccountInfo.DATE_OF_BIRTH], other_info[AccountInfo.GENDER]
                )

        cursor.execute(create_user_command)
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

def create_post(email, title, body, category, website):
    """
    Create a post for username 
    This function will create a post for 'username' and insert this post into our database.
    """
    try:
        connection_handler = website.mysql_server.connect()
        cursor = connection_handler.cursor()
        cursor.execute('SELECT * FROM {} WHERE {} = "{}"'.format(DatabaseModel.USER, AccountInfo.EMAIL, email))
        for user in cursor:
            user_id = str(user[0])

        command = 'INSERT INTO {}({}, {}, {}, {}) VALUES("{}", "{}", "{}", "{}");'.format(DatabaseModel.POST,
            PostInfo.CATEGORY_ID, PostInfo.POST_TEXT, PostInfo.POST_TITLE, PostInfo.USER_ID,
            category, body, title, user_id)

        cursor.execute(command)
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


def get_category_list(website):
    connection_handler = website.mysql_server.connect()
    cursor = connection_handler.cursor()
    cursor.execute("SELECT * FROM {}".format(DatabaseModel.CATEGORY))
    result = cursor.fetchall()
    category_list = [list(i) for i in result]
    
    return category_list

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

def get_all_posts(website, order=None, filter_dict=None):
    """
    Query database for list(post_id)
    If the our database does NOT exist post_id, return False and return function, print("Error: ERROR_CODE[2]) -> False
    """
    try:
        connection_handler = website.mysql.connect()
        cursor = connection_handler.cursor()

        fetch_all_posts_command = 'SELECT * FROM {0} INNER JOIN {1} on {0}.{2} = {1}.{3}'.format(
            DatabaseModel.POST, DatabaseModel.USER, PostInfo.USER_ID, AccountInfo.USER_ID)

        order_command = ''
        if order != None:
            order_command = 'ORDER BY {} DESC'.format(order)

        filter_command = ''
        if filter_dict != None:
            decompose_arr = []
            for key in filter_dict:
                individual_query = '{} = {}'.format(key, filter_dict[key])
                decompose_arr.append(individual_query)
            filter_str = 'WHERE' + 'AND'.join(decompose_arr)
            filter_command = filter_str

        query_command = ' '.join([fetch_all_posts_command, order_command, filter_command])
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

