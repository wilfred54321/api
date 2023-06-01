class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///api.db'
    SECRET_KEY = '92a6ede02ad2f80c0278447bffd258ad84dbefc4746d6dfc9c328d4acaa0360c'
    SQLALCHEMY_TRACK_MODIFICATIONS= False
    TEMPLATES_AUTO_RELOAD = True
    API_ADMIN_LOGS = './api/static/logs/admin.log'
    MAIN_LOGS = './api/static/logs/main.log'
    USERS_LOGS = './api/static/logs/users.log'
    API_USERS_LOGS = './api/static/logs/api_users.log'
    JOKES_LOGS = './api/static/logs/jokes.log'






