class WebsiteLoginStatus:
    LOGGED_IN = 'logged_in'
    LOGGED_USER_EMAIL = 'logged_user_email'
    
class ErrorCode:
    SUCCESS: "success!"
    OPERATION_NOT_PERMITTED: "user does not permission to delete this post/comment"
    POST_NOT_EXIST: "post/comment does not exist!"

# Database Model NAME
class DatabaseModel:
    USER = 'user'
    POST = 'post'
    COMMENT = 'comment'
    CATEGORY = 'category'

# Database Model related keyword
class AccountInfo:
    USERNAME = 'username'
    USER_ID = 'user_id'
    EMAIL = 'email_id'
    PASSWORD = 'password'
    PHONE = 'phone'
    DATE_OF_BIRTH = 'dob'
    GENDER = 'gender'

class PostInfo:
    POST_ID  = 'post_id'
    USER_ID = 'user_id'
    POST_TITLE = 'post_title'
    POST_TEXT = 'post_text'
    CATEGORY_ID = 'category_id'
    TIMESTAMP = 'timestamp'

class CategoryInfo:
    CATEGORY_ID = 'category_id'
    VALUE = 'value'

class CommentInfo:
    COMMENT_ID = 'comment_id'
    POST_ID = 'post_id'
    USER_ID = 'user_id'
    COMMENT_TEXT = 'comment_text'
    TIMESTAMP = 'timestamp'