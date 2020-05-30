from flask import request, render_template, redirect, url_for
from flask.blueprints import Blueprint
from flask_login import current_user, login_user, logout_user, login_required

from cmdbmix.models.auth import User
from cmdbmix.forms.auth import LoginForm

soft_bp = Blueprint('soft', __name__)


@soft_bp.route('/soft_manager', methods=['GET'])
@login_required
def soft_manager():
    return render_template('cmdb/software.html')