from ConstantTable import DefaultFileInfo, AppConfigurationKey
import WebsiteAPI
import os

class Website:
    def __init__(self, app, mysql_server):
        self.app = app
        self.mysql_server = mysql_server
        self.config = {}
        self.stored_account_info = {}

        self.config_app()

    def config_app(self):
        self.allowed_file_type = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
        app_script_path = os.path.abspath(__file__)
        app_script_dir_path = os.path.dirname(app_script_path)
        self.upload_folder = WebsiteAPI.get_relative_path([0, [app_script_dir_path, 'static', 'profile_pics']])

        self.app.config[AppConfigurationKey.UPLOAD_FOLDER] = self.upload_folder

        self.app.config[AppConfigurationKey.DATABASE_HOST] = 'localhost'
        self.app.config[AppConfigurationKey.DATABASE_USER] = 'root'
        self.app.config[AppConfigurationKey.DATABASE_PASSWORD] = 'root123'
        self.app.config[AppConfigurationKey.DATABASE_DB] = 'web_forum'
        self.app.secret_key = 'super secret key'
        self.mysql_server.init_app(self.app)
