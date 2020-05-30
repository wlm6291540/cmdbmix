from flask import request, render_template, redirect, url_for
from flask.blueprints import Blueprint
from flask_login import current_user, login_user, logout_user, login_required

from cmdbmix.models.auth import User, Role
from cmdbmix.forms.auth import LoginForm

role_bp = Blueprint('role', __name__)


@role_bp.route('/role_manager', methods=['GET'])
@login_required
def role_manager():
    roles = Role.query.all()
    return render_template('perms/role.html', roles=roles)



@role_bp.route('/role_manger/bind_user', methods=['GET'])
@login_required
def bind_user():
    roles = Role.query.all()
    return render_template('perms/bind_role.html')
