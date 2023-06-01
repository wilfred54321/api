from flask import Blueprint, render_template,request,redirect,url_for,flash
from api import db, alias
from . import logger
from api.models import User, Role, App, Key, Status
from flask_login import login_required, current_user

api_user = Blueprint('api_user', __name__, template_folder='templates')


@login_required
@api_user.route('/dashboard')
def dashboard():
    if current_user.is_authenticated:
        user = current_user._get_current_object()



        # result = db.session.query(User,App,Key).select_from(User).join(App).join(Key).filter(User.user_id == 2).all()
        query_result = db.session.query(User, Role, Status, App, Key, db.func.count(App.api_keys)).select_from(User).outerjoin(Role).filter(User.user_id == user.user_id).outerjoin(Status).outerjoin(App).outerjoin(Key).group_by(App.name).all()

        total_api_keys = db.session.query(db.func.count(App.api_keys)).select_from(User).outerjoin(App).filter(User.user_id == user.user_id).outerjoin(Key).group_by(User.user_id).one()
        api_key_count = total_api_keys[0]

        return render_template("api_user_index.html", data=query_result,api_key_count = api_key_count)
    return render_template('401.html')


@login_required
@api_user.route('/add_application', methods = ['POST','GET'])
def add_application():
    user = current_user._get_current_object()

    if request.method == 'POST':
        #get input from user
        app_name = request.form.get('name')
        app_description = request.form.get('description')
        app = App(name = app_name,description = app_description,user_id = user.user_id)
        db.session.add(app)
        db.session.commit()
        flash(f'{app.name} added successfully','success')
        logger.info(f"{user.email} added application with name '{app.name}'")
        return redirect(request.referrer)

    if request.method == "GET":
        apps = db.session.query(App).select_from(App).join(User).filter(User.user_id == user.user_id).all()


         #TO BE REMOVED
        query_result = db.session.query(User, Role, Status, App, Key, db.func.count(App.api_keys)).select_from(User).outerjoin(Role).filter(User.user_id == user.user_id).outerjoin(Status).outerjoin(App).outerjoin(Key).group_by(App.name).all()

        total_api_keys = db.session.query(db.func.count(App.api_keys)).select_from(User).outerjoin(App).filter(User.user_id == user.user_id).outerjoin(Key).group_by(User.user_id).one()
        api_key_count = total_api_keys[0]
        return render_template("create_application.html",apps = apps,data = query_result)


@login_required
@api_user.route('/edit_application', methods = ['POST','GET'])
def edit_application():
    user = current_user._get_current_object()
    if request.method == 'POST':

        app_id = int(request.form.get('app'))
        name = request.form.get('name')
        description = request.form.get('description')

        app = App.query.filter_by(app_id = app_id).first()
        old_app_name = app.name
        app.name = name
        app.description = description
        db.session.commit()
        flash(f'{old_app_name} edited successfully','success')
        logger.info(f"{user.email} edited application with name '{app.name}'")

        return redirect (url_for('api_user.dashboard'))
    apps = db.session.query(App).select_from(App).join(User).filter(User.user_id == user.user_id).all()

    query_result = db.session.query(User, Role, Status, App, Key, db.func.count(App.api_keys)).select_from(User).outerjoin(Role).filter(User.user_id == user.user_id).outerjoin(Status).outerjoin(App).outerjoin(Key).group_by(App.name).all()

    total_api_keys = db.session.query(db.func.count(App.api_keys)).select_from(User).outerjoin(App).filter(User.user_id == user.user_id).outerjoin(Key).group_by(User.user_id).one()
    api_key_count = total_api_keys[0]

    return render_template('edit_application.html',apps = apps,data = query_result)



@login_required
@api_user.route('/delete_app', methods = ['POST','GET'])
def delete_app():
    input = request.form.getlist('checkbox')

    print(input)
    exit()


@login_required
@api_user.route('/add_key', methods = ['POST'])
def add_api_key():
    user = current_user._get_current_object()
    app_id = int(request.form.get('app'))
    app = App.query.filter_by(app_id = app_id).first()
    app.add_key()
    flash(f'Key added successfully to app {app.name}','success')
    logger.info(f"{user.email} added api key to application with name '{app.name}'")

    return redirect (url_for('api_user.dashboard'))


@login_required
@api_user.route('/edit_key', methods = ['POST'])
def edit_api_key():
    user = current_user._get_current_object()
    if request.method == "POST" and request.form.get('key'):
        old_keys = request.form.getlist('checkbox')
        new_key = request.form.get('key')
        old_key = int(old_keys[0])
        app = db.session.query(App).select_from(App).join(Key).filter(Key.key_id == old_key).first()
        key = Key.query.filter_by(key_id = old_key).first()
        key.key = new_key
        db.session.commit()
        flash(f'Key updated successfully to app {app.name}','success')
        logger.info(f"{user.email} updated api key for application with name '{app.name}'")


    if request.method == "POST":
        app_id = request.form.get('app')
        keys = db.session.query(Key).select_from(Key).join(App).filter( App.app_id == app_id).all()
        apps = db.session.query(App).select_from(App).join(User).filter(User.user_id == user.user_id).all()

        return render_template("edit_application.html",keys = keys,apps = apps)

