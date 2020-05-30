from flask import request, render_template, redirect, url_for
from flask.blueprints import Blueprint
from flask_login import current_user, login_user, logout_user, login_required

from cmdbmix.models.auth import User
from cmdbmix.forms.auth import LoginForm

user_bp = Blueprint('user', __name__)


@user_bp.route('/user_manager', methods=['GET'])
@login_required
def user_manager():
    return render_template('perms/user.html')
