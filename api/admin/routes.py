from flask import Blueprint,render_template
from flask_login import login_required,current_user
from api.models import User,Role,Status,App,Key,json_formatter
from api import db
import json

admin = Blueprint('admin',__name__,template_folder='templates')

@login_required
@admin.route('/dashboard')
def dashboard():
    if current_user.is_authenticated:
        result = db.session.query(User,Role,Status).select_from (User).join(Role).join(Status).limit(5).all()
        return render_template("admin_index.html",users = result)
    return render_template('401.html')

@login_required
@admin.route("/users")
def users():
    # result = db.session.query(User,Role,Status).select_from (User).join(Role).join(Status).all()
    # result = db.session.query(User,Role,Status).select_from (User).join(Role).join(Status).all()

    query_result = db.session.query(User,Role,Status,App,Key,db.func.count(App.app_id),db.func.count(Key.key_id)).\
        select_from (User).outerjoin(Role).outerjoin(Status).outerjoin(App).outerjoin(Key).\
        group_by(User.user_id).all()

    return render_template("users.html",result = query_result)


@login_required
@admin.route("/charts")
def charts():

    return render_template("charts.html")
