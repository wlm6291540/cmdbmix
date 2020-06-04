from flask import request, render_template, redirect, url_for, jsonify
from flask.blueprints import Blueprint
from flask_login import login_required

from cmdbmix.decorators import auth_required
from cmdbmix.models.auth import User, Role
from cmdbmix.forms.auth import LoginForm, UserEditForm, UserAddForm
from cmdbmix.utils import get_page_args

user_bp = Blueprint('user', __name__)


@user_bp.route('/user_manager', methods=['GET'])
@login_required
@auth_required
def user_manager():
    page, per_page = get_page_args(request)
    pagination = User.query.order_by('id').paginate(page, per_page=per_page)
    users = pagination.items
    return render_template('perms/user.html', users=users, pagination=pagination)


@user_bp.route('/user_manager/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
@auth_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    roles = Role.query.all()
    form = UserEditForm()
    form.role_id.choices = [(str(role.id), role.name) for role in roles]
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
    form.role_id.data = user.role_id
    form.is_active.data = user.is_active
    return render_template('perms/edit_user.html', user=user, form=form)


@user_bp.route('/user_manager/active_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
@auth_required
def active_user(user_id):
    user = User.query.get_or_404(user_id)
    user.is_active = not user.is_active
    user.save()
    return redirect(url_for('user.user_manager'))



@user_bp.route('/user_manager/add_user', methods=['GET', 'POST'])
@login_required
@auth_required
def add_user():
    form = UserAddForm()
    form.role_id.choices = [(str(role.id), role.name) for role in Role.query.all()]
    if form.validate_on_submit():
        user = User()
        if form.role_id.data is not None:
            user.role = Role.query.get_or_404(form.role_id.data)
        if form.password.data is not None:
            user.set_password(form.password.data)
        user.username = form.username.data
        user.nickname = form.nickname.data.strip()
        user.email = form.email.data.strip()
        user.is_active = form.is_active.data
        user.generate_avatar()
        user.save()
        return redirect(url_for('user.user_manager'))
    return render_template('perms/add_user.html',form=form)


@user_bp.route('/user_manager/delete_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
@auth_required
def delete_user(user_id):
    User.query.get_or_404(user_id).delete()
    return redirect(url_for('user.user_manager'))