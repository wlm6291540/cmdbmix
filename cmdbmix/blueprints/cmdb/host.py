from flask import request, render_template, redirect, url_for
from flask.blueprints import Blueprint
from flask_login import current_user, login_user, logout_user, login_required

from cmdbmix.models.auth import User
from cmdbmix.forms.auth import LoginForm

host_bp = Blueprint('host', __name__)


@host_bp.route('/host_manager', methods=['GET'])
@login_required
def host_manager():
    return render_template('cmdb/host.html')