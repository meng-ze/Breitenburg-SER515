from ConstantTable import AccountInfo, PostInfo

# ---
# class Account <Database>
"""
        *** not finished yet ***
"""
def verify_login_password(email, password, website):
    try:
        connection_handler = website.mysql_server.connect()
        cursor = connection_handler.cursor()
        cursor.execute("SELECT * FROM user WHERE %s = %s and %s = %s", (
            AccountInfo.EMAIL, email, AccountInfo.PASSWORD, password)
        )
        for email_id in cursor:
            print("{}".format(email_id))
            cursor.close()
            return True

    except Exception as e:
        print('Error!')
        print(e)

    if cursor != None:
        cursor.close()
    return False

def create_account(username: str, other_info: {str: None}, website):
    cursor = None
    try:
        connection_handler = website.mysql_server.connect()
        cursor = connection_handler.cursor()
        cursor.execute("INSERT INTO user(%s, %s, %s, %s, %s, %s) VALUES(%s, %s, %s, %s, %s, %s)", (
            AccountInfo.USERNAME, AccountInfo.EMAIL, AccountInfo.PASSWORD,
            AccountInfo.PHONE, AccountInfo.DATE_OF_BIRTH, AccountInfo.GENDER,

            username, other_info[AccountInfo.EMAIL], other_info[AccountInfo.PASSWORD],
            other_info[AccountInfo.PHONE], other_info[AccountInfo.DATE_OF_BIRTH], other_info[AccountInfo.GENDER])
        )
        connection_handler.commit()
        cursor.close()

    except Exception as e:
        print('Error!')
        print(e)
        if cursor != None:
            cursor.close()
        return False

    return True

# def modify_account(username: str, key: str, value: None)
# def delete_account(username: str)
# def get_account_info(username: str) -> {str: None}

# ---
# class Post <Database>
""" Actions below SHOULD include timestamp """

def create_post(email, title, body, category, timestamp, website):
    """
    Create a post for username 
    This function will create a post for 'username' and insert this post into our database.
    """
    try:
        connection_handler = website.mysql_server.connect()
        cursor = connection_handler.cursor()
        cursor.execute("SELECT * FROM user WHERE %s = %s", (AccountInfo.EMAIL, email))
        for user in cursor:
            user_id = str(user[0])
        connection_handler = website.mysql_server.connect()
        cursor= connection_handler.cursor()
        cursor.execute("INSERT INTO post(%s, %s, %s, %s, %s) VALUES(%s, %s, %s, %s, %s)", (
            PostInfo.CATEGORY_ID, PostInfo.POST_TEXT, PostInfo.POST_TITLE, PostInfo.TIMESTAMP, PostInfo.USER_ID,
            category, body, title, timestamp, user_id)
        )
        connection_handler.commit()
        cursor.close()

    except Exception as e:
        print('Error!')
        print(e)
        if cursor != None:
            cursor.close()
        return False

    return True

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

# def get_posts([post_id: address]) -> list(Post):
#     """
#     Query database for list(post_id)
#     If the our database does NOT exist post_id, return False and return function, print("Error: ERROR_CODE[2]) -> False
#     """
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

