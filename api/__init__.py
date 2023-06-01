from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import alias
from api.config import Config


# from api.main.models import User,Role

db = SQLAlchemy()
login_manager = LoginManager()



# import logging
# # logging.basicConfig(level=logging.INFO,filename="api.log",
# #                     format = '%(asctime)s] %(levelname)s in %(module)s: %(message)s')
# #
# # logging configuration
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)
#
# formatter = logging.Formatter('%(asctime)s] %(levelname)s in %(module)s: %(message)s')
#
# file_handler = logging.FileHandler('api.log')
# file_handler.setFormatter(formatter)
#
# logger.addHandler(file_handler)

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)
    db.init_app(app)
    login_manager.init_app(app)




    from .main.routes import main
    from .users.routes import users
    from .jokes.routes import jokes
    from .admin.routes import admin
    from .api_user.routes import api_user

    app.register_blueprint(main)
    app.register_blueprint(users,url_prefix = "/users")
    app.register_blueprint(jokes,url_prefix = "/api/jokes")
    app.register_blueprint(admin,url_prefix ="/admin")
    app.register_blueprint(api_user,url_prefix = "/api_user")
    return app


