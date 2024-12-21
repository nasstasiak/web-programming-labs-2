from flask import  render_template, Blueprint, request, redirect 
from datetime import datetime
from db import db
from db.models import users, articles
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, login_required, current_user, logout_user

lab8 = Blueprint('la9', __name__)


@lab8.route('/lab9/')
def main():
    return render_template('lab9/lab9.html')