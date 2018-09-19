---
class Account <Database>

def create_account(username: str, other_info: {str: None})
def modify_account(username: str, key: str, value: None)
def delete_account(username: str)
def get_account_info(username: str)

---
class Post <Database>
""" Create anything should include timestamp """

def create_post(username: Account, descript: str) -> post_id
def modify_post(username: Account, post_id: address, description: str)
def delete_post(username: Account, post_id: address)
def delete_comment(username: Account, post_id: address, description: str)

def get_posts([post_id: address]) -> list(Post)
def query_by_keyword(keyword) -> list(Post)
def query_by_username(username) -> list(Post)
def query_by_date_range(start_date, end_date) -> list(Post)

?? def upload_file(filepath: str, media_type: str, attached_post: Post)

