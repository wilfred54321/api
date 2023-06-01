from flask import Blueprint, session
from . import logger


from api.models import User,Role,Key
from api.main.utils import json_formatter
from flask import make_response,jsonify,request,render_template,flash,redirect,url_for
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,current_user,login_required,logout_user

users = Blueprint("users",__name__,template_folder="templates")


@users.route("/register",methods = ['GET','POST'])
def register():
    if request.method == 'POST':
        #get input from users and process application
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        email = request.form.get('email')
        password = generate_password_hash(request.form.get('password'))

        role = request.form.get("role")
        user_args = {"firstname":firstname,
                     "lastname":lastname,
                     "email":email,
                     "password":password,
                     "role_id":role}
        user = User()

        try:
            user.add_user(**user_args)
        except:
            message = f"error occured - user {email}  may already exist"
            flash(message,'danger')
            logger.error(message)
        else:
            message = f"user with email {email}  added successfully"
            flash(message,"success")
            logger.info(message)
        finally:
            return redirect(request.referrer)

    # get roles from database and populate the registration field
    roles = Role.query.all()
    return render_template("register.html",roles = roles)




@users.route("/login", methods = ['GET','POST'])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email = email).first()
        if user and check_password_hash(user.password,password):
            login_user(user)
            logger.info(f"User {user.firstname} logged in")
            flash("You have logged in successfully",'success')
            # check the user role
            if user.user_role() == user.get_user_role():
                # get the blueprint name

                return redirect(url_for(f"{user.get_user_role()}.dashboard"))
            # if user.user_role() == "admin":
            #     return redirect(url_for("admin.dashboard"))
            # if user.user_role() == "api_user":
            #     return redirect(url_for("users.api_user_profile"))
            # if user.user_role() == "developer":
            #     return redirect(url_for('users.api_developer_profile'))

    return render_template("login.html")
        # check if this is correct
        # user = User.query.filter_by(email = email).first()
        # print(user)



@login_required
@users.route("/admin",methods =['GET','POST'])
def admin_profile():
    return f"You are logged in as an admin {current_user.email}"

@login_required
@users.route("/api_user",methods =['GET','POST'])
def api_user_profile():
    return f"You are logged in as an api_user {current_user.email}"

@login_required
@users.route("/api_developer",methods =['GET','POST'])
def api_developer_profile():
    return f"You are logged in as a developer {current_user.email}"

@login_required
@users.route("/logout")
def logout():

    logger.info(f"{current_user.email} logged out")
    logout_user()
    flash("You'hv been logged out","info")
    return redirect(url_for("users.login"))


@users.route("/password")
def forgot_password():
    return render_template('password.html')


      #get input and validate user


# @users.route("/all")
# def all_users():
#     users = []
#     response = User.query.all()
#     for user in response:
#         user = json_formatter(user)
#         users.append(user)
#     return make_response(jsonify(users),200)
#
#
# @users.route("/<int:user_id>", methods = ['GET','PUT','UPDATE','DELETE'])
# def one_user(user_id):
#
#         user = User.query.filter_by(user_id = user_id).first()
#         if user:
#             if request.method == "GET":
#                 user = json_formatter(user)
#                 return make_response(jsonify(user),200)
#
#
#             if request.method == "DELETE":
#                 db.session.delete(user)
#                 db.session.commit()
#                 return make_response("Success",200)
#
#         return make_response("The requested resource was not found", 404)
#
#
# @users.route("/add", methods = ['POST'])
# def add_user():
#     content = request.json
#     if request.method == "POST":
#     # check if user already exist
#         user = User.query.filter_by(email = content['email']).first()
#         if user is None:
#     # proceed to insert user in the database
#             new_user = User(
#                 firstname = f"{content['firstname']}",
#                 lastname = f"{content['lastname']}",
#                 password = f"{content['password']}",
#                 email = f"{content['email']}",
#                 role_id = f"{content['role_id']}")
#             db.session.add(new_user)
#             db.session.commit()
#             return make_response("user added successfully", 200)
#         return make_response("user already exists",301)
#
#
# from sqlalchemy import func
# @users.route("/count", methods=['GET'])
# def user_count():
#     if request.method == "GET":
#         users  = User.query.all()
#         row_count = len(users)
#         return make_response(jsonify(row_count))
#
