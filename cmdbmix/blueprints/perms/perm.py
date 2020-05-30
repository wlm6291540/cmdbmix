from flask import request, render_template, redirect, url_for
from flask.blueprints import Blueprint
from flask_login import current_user, login_user, logout_user, login_required

from cmdbmix.models.auth import User
from cmdbmix.forms.auth import LoginForm

perm_bp = Blueprint('perm', __name__)


@perm_bp.route('/perm_manager', methods=['GET'])
@login_required
def perm_manager():
    return render_template('perms/perm.html')

