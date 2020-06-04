from flask import request, render_template, redirect, url_for
from flask.blueprints import Blueprint
from flask_login import current_user, login_user, logout_user, login_required

from cmdbmix.models.cmdb import db, Tag
from cmdbmix.forms.auth import LoginForm

db_bp = Blueprint('db', __name__)


@db_bp.route('/db_manager', methods=['GET'])
@login_required
def db_manager():
    return render_template('cmdb/database.html')