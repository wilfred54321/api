import json
from api import db,login_manager
from flask_login import login_required
from datetime import datetime
import secrets


class Role(db.Model):
    __tablename__ = "roles"
    role_id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    users = db.relationship('User', backref='roles',cascade = "all,delete")


class Status(db.Model):
    __tablename__ = "status"
    status_id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String, nullable=False)


class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column(db.String, nullable=False)
    lastname = db.Column(db.String, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    status_id = db.Column(db.Integer, db.ForeignKey('status.status_id'), nullable=False, default=1)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.role_id"), nullable=False, default=1)
    apps = db.relationship('App', backref='user',cascade = "all,delete")

    def add_user(self,firstname,lastname,email,password,role_id):
        user = User(firstname = firstname,
                    lastname = lastname,
                    email = email,
                    password = password,
                    role_id = role_id)

        if not self.user_exists():
            db.session.add(user)
            db.session.commit()

        # check if user already exist
    def user_exists(self):
        user =User.query.filter_by(email = self.email).first()
        if user:
            return True
        return False


        #check user role
    def user_role(self):
        if self.role_id == 1:
            return "admin"
        if self.role_id == 2:
            return "api_user"
        if self.role_id == 3:
            return "developer"

    def get_user_role(self):
        return self.user_role()

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def get_id(self):
        return self.user_id

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)




class App(db.Model):
    __tablename__ = 'apps'
    app_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable = False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    api_keys = db.relationship('Key', backref="keys",cascade = "all,delete")

    def add_app(self,name,description,user_id):
        app = App(name = name,
                    description = description,
                    user_id = user_id,)
        if not self.app_exists():
            db.session.add(app)
            db.session.commit()

    def app_exists(self):
        app = App.query.filter_by(app_id = self.app_id).first()
        if app:
            return True
        return False


    def add_key(self):
        return Key.add_key(self)



class Key(db.Model):
    __tablename__ = 'apikeys'
    key_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    key = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    app_id = db.Column(db.Integer, db.ForeignKey('apps.app_id'),nullable = False)

    def add_key(self):
        key = Key(key = Key.generate_key(),app_id = self.app_id)
        db.session.add(key)
        db.session.commit()


    @staticmethod
    def generate_key():
        key = secrets.token_hex(32)
        return key

def json_formatter(data):
    result =json.dumps([{"user": record[0],
              "role": record[1],
              "status": record[2],
              "app": record[3],
              "key": record[4],
              "app_count":record[5],
              "key_count":record[6]} for record in data])
    return result
