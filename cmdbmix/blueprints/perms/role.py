from flask import request, render_template, redirect, url_for, jsonify
from flask.blueprints import Blueprint
from flask_login import current_user, login_user, logout_user, login_required

from cmdbmix.decorators import auth_required
from cmdbmix.models.auth import User, Role, Permission
from cmdbmix.forms.auth import LoginForm, RoleEditForm
from cmdbmix.utils import format_form_errors, get_page_args

role_bp = Blueprint('role', __name__)


@role_bp.route('/role_manager', methods=['GET'])
@login_required
@auth_required
def role_manager():
    page, per_page = get_page_args(request)
    pagination = Role.query.order_by('id').paginate(page, per_page=per_page)
    roles = pagination.items
    return render_template('perms/role.html', roles=roles, pagination=pagination)


@role_bp.route('/role_manager/bind_user/<int:role_id>', methods=['GET', 'POST'])
@login_required
@auth_required
def bind_user(role_id):
    role = Role.query.get_or_404(role_id)
    if request.method == 'POST':
        if not request.is_json:
            return jsonify({'msg': '参数格式不正确'}), 400
        ids = request.json
        for user_id in ids:
            user = User.query.get_or_404(user_id)
            if user in role.users:
                role.users.remove(user)
            else:
                role.users.append(user)
        role.save()
        return jsonify({'msg': '绑定成功'}), 200
    elif request.method == 'GET':
        unbind_user = User.query.filter(User.role_id != role.id).all() + User.query.filter_by(role_id=None).all()
        return render_template('perms/bind_role.html', left_title="未绑定用户", right_title="已绑定用户", role=role,
                               binds=role.users, unbinds=unbind_user)


@role_bp.route('/role_manager/bind_perm/<int:role_id>', methods=['GET', 'POST'])
@login_required
@auth_required
def bind_perms(role_id):
    role = Role.query.get_or_404(role_id)
    if request.method == 'POST':
        if not request.is_json:
            return jsonify({'msg': '参数格式不正确'}), 400
        ids = request.json
        for perm_id in ids:
            perm = Permission.query.get_or_404(perm_id)
            if perm in role.permissions:
                role.permissions.remove(perm)
            else:
                role.permissions.append(perm)
        role.save()
        return jsonify({'msg': '绑定成功'}), 200
    elif request.method == 'GET':
        perms_id = [perm.id for perm in role.permissions]
        print(perms_id)
        unbind_perms = Permission.query.filter(Permission.id.notin_(perms_id)).all()
        return render_template('perms/bind_perms.html', left_title="未绑定权限", right_title="已绑定权限", role=role,
                               binds=role.permissions, unbinds=unbind_perms)


@role_bp.route('/role_manager/edit_role/<int:role_id>', methods=['GET', 'POST'])
@login_required
@auth_required
def edit_role(role_id):
    form = RoleEditForm()
    role = Role.query.get_or_404(role_id)
    if form.validate_on_submit():
        role.name = form.name.data
        role.desc = form.desc.data
        role.save()
        return redirect(url_for('role.role_manager'))
    form.desc.data = role.desc
    return render_template('perms/edit_role.html', role=role, form=form)


@role_bp.route('/role_manager/add_role', methods=['GET', 'POST'])
@login_required
@auth_required
def add_role():
    form = RoleEditForm()
    if form.validate_on_submit():
        role = Role()
        role.name = form.name.data
        role.desc = form.desc.data
        role.save()
        return redirect(url_for('role.role_manager'))
    return render_template('perms/add_role.html', form=form)



@role_bp.route('/role_manager/delete_role/<int:role_id>', methods=['GET', 'POST'])
@login_required
def delete_role(role_id):
    Role.query.get_or_404(role_id).delete()
    return redirect(url_for('role.role_manager'))
