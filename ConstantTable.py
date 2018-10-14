from enum import Enum

class WebsiteLoginStatus(Enum):
    LOGGED_IN = 'logged_in'
    LOGGED_USER_EMAIL = 'logged_user_email'
    
class AccountInfo(Enum):
    USERNAME = 'username'
    USER_ID = 'user_id'
    EMAIL = 'email_id'
    PASSWORD = 'password'
    PHONE = 'phone'
    DATE_OF_BIRTH = 'dob'
    GENDER = 'gender'

class PostInfo(Enum):
    POST_ID  = 'post_id'
    USER_ID = 'user_id'
    POST_TITLE = 'post_title'
    POST_TEXT = 'post_text'
    CATEGORY_ID = 'category_id'
    TIMESTAMP = 'timestamp'

class ErrorCode(Enum):
    SUCCESS: "success!"
    OPERATION_NOT_PERMITTED: "user does not permission to delete this post/comment"
    POST_NOT_EXIST: "post/comment does not exist!"
