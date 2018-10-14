from enum import Enum

class AccountInfo(Enum):
    USERNAME = 'username'
    EMAIL = 'email_id'
    PASSWORD = 'password'
    PHONE = 'phone'
    DATE_OF_BIRTH = 'dob'
    GENDER = 'gender'

class ErrorCode(Enum):
    SUCCESS: "success!"
    OPERATION_NOT_PERMITTED: "user does not permission to delete this post/comment"
    POST_NOT_EXIST: "post/comment does not exist!"
