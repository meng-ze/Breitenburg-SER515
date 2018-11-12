class Website:
    def __init__(self, app, mysql_server):
        self.app = app
        self.mysql_server = mysql_server
        self.config = {}
        self.stored_account_info = {}

        self.config_app()

    def config_app(self):
        self.app.config['MYSQL_DATABASE_HOST'] = 'localhost'
        self.app.config['MYSQL_DATABASE_USER'] = 'root'
        self.app.config['MYSQL_DATABASE_PASSWORD'] = ''
        self.app.config['MYSQL_DATABASE_DB'] = 'web_forum'
        self.app.secret_key = 'super secret key'
        self.mysql_server.init_app(self.app)
