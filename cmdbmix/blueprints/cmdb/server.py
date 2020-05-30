from flask import request, render_template, redirect, url_for
from flask.blueprints import Blueprint
from flask_login import current_user, login_user, logout_user, login_required

from cmdbmix.models.auth import User
from cmdbmix.forms.auth import LoginForm

server_bp = Blueprint('server', __name__)


@server_bp.route('/server_manager', methods=['GET'])
@login_required
def server_manager():
    return render_template('cmdb/server.html')