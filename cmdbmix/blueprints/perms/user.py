from flask import request, render_template, redirect, url_for, jsonify
from flask.blueprints import Blueprint
from flask_login import current_user, login_user, logout_user, login_required

from cmdbmix.models.auth import User, Role
from cmdbmix.forms.auth import LoginForm, UserEditForm

user_bp = Blueprint('user', __name__)


@user_bp.route('/user_manager', methods=['GET'])
@login_required
def user_manager():
    users = User.query.all()
    return render_template('perms/user.html', users=users)


@user_bp.route('/user_manager/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    roles = Role.query.all()
    form = UserEditForm()
    if form.validate_on_submit():
        if form.role_id.data is not None:
            user.role = Role.query.get_or_404(form.role_id.data)
        if form.password.data is not None:
            user.set_password(form.password.data)
        user.nickname = form.nickname.data.strip()
        user.email = form.email.data.strip()
        user.is_active = form.is_active.data
        user.save()
        return redirect(url_for('user.user_manager'))
    return render_template('perms/edit_user.html', user=user, roles=roles, form=form)


@user_bp.route('/user_manager/active_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def active_user(user_id):
    user = User.query.get_or_404(user_id)
    user.is_active = not user.is_active
    user.save()
    return redirect(url_for('user.user_manager'))
