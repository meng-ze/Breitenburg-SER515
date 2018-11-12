class WebsiteLoginStatus:
    LOGGED_IN = 'logged_in'
    LOGGED_USER_EMAIL   = 'logged_user_email'
    LOGGED_USER_ID      = 'logged_user_id'
    LOGGED_USER_ROLE_ID = 'role'
    
class ErrorCode:
    ERROR_CODE = 'error code'
    PASSWORD_INCORRECT = 'password incorrect'
    SUCCESS = 'success!'
    OPERATION_NOT_PERMITTED = 'user does not permission to delete this post/comment'
    POST_NOT_EXIST = 'post/comment does not exist!'
    USER_IS_BLOCKED = 'user is blocked'
    USER_NOT_EXIST = 'user does not exist'

# Database Model NAME
class DatabaseModel:
    USER = 'user'
    USER_ROLE = 'user_role'
    POST = 'post'
    COMMENT = 'comment'
    CATEGORY = 'category'
    BLOCK_USER = 'blocked_user'

# Database Model related keyword
class AccountInfo:
    USERNAME = 'username'
    USER_ID = 'user_id'
    USER_ROLE_ID = 'user_role'
    EMAIL = 'email_id'
    PASSWORD = 'password'
    PHONE = 'phone'
    DATE_OF_BIRTH = 'dob'
    GENDER = 'gender'

class AccountRoleInfo:
    ID = 'id'
    USER_ROLE = 'user_role'

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

class BlockInfo:
    EMAIL = 'email_id'