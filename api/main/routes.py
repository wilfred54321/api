from flask import Blueprint,render_template,request
from api import db
from . import logger
from api.models import Key,App
from flask_login import current_user
from flask_login import login_required


main = Blueprint('main',__name__,template_folder="templates")

@main.route("/")
def index():
    logger.info("Index accessed!")
    return "My api works! Yippie!!!!"

@main.route("/create_tables")
def create_tables():
    db.create_all()
    return "OK"


