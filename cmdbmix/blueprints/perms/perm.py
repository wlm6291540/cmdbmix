from flask import request, render_template, redirect, url_for, current_app
from flask.blueprints import Blueprint
from flask_login import current_user, login_user, logout_user, login_required

from cmdbmix.decorators import auth_required
from cmdbmix.models.auth import User, Permission, Role
from cmdbmix.forms.auth import LoginForm, PermEditForm, PermAddForm
from cmdbmix.utils import perm_to_list, get_page_args

perm_bp = Blueprint('perm', __name__)


@perm_bp.route('/perm_manager', methods=['GET'])
@login_required
@auth_required
def perm_manager():
    page, per_page = get_page_args(request)
    pagination = Permission.query.order_by('url').paginate(page=page, per_page=per_page)
    perms = pagination.items
    return render_template('perms/perm.html', perms=perms, pagination=pagination)


@perm_bp.route('/perm_manager/edit_perm/<int:perm_id>', methods=['GET', 'POST'])
@login_required
@auth_required
def edit_perm(perm_id):
    perm = Permission.query.get_or_404(perm_id)
    form = PermEditForm()
    form.url.choices = sorted([(item.endpoint, item.endpoint) for item in current_app.url_map.iter_rules()])
    if form.validate_on_submit():
        perm.name = form.name.data
        perm.url = form.url.data
        perm.type = form.type.data
        perm.desc = form.desc.data
        perm.save()
        return redirect(url_for('perm.perm_manager'))
    form.url.data = perm.url
    form.type.data = perm.type
    return render_template('perms/edit_perm.html', perm=perm, form=form)


@perm_bp.route('/perm_manager/add_perm', methods=['GET', 'POST'])
@login_required
@auth_required
def add_perm():
    form = PermAddForm()
    form.role.choices = [(str(role.id), role.name) for role in Role.query.all()]
    form.url.choices = sorted(filter_url([(item.endpoint, item.rule) for item in current_app.url_map.iter_rules()]))
    if form.validate_on_submit():
        perm = Permission()
        perm.name = form.name.data
        perm.url = form.url.data
        perm.type = form.type.data
        perm.desc = form.desc.data
        if form.role.data:
            perm.roles.append(Role.query.get_or_404(form.role.data))
        perm.save()
        return redirect(url_for('perm.perm_manager'))
    urls = current_app.url_map.iter_rules()
    return render_template('perms/add_perm.html', form=form, urls=urls)


@perm_bp.route('/perm_manager/delete_perm/<int:perm_id>', methods=['GET', 'POST'])
@login_required
@auth_required
def delete_perm(perm_id):
    perm = Permission.query.get_or_404(perm_id)
    perm.delete()
    return redirect(url_for('perm.perm_manager'))


def filter_url(items):
    perms = [perm.url for perm in Permission.query.all()]
    ret = []
    for end, rule in items:
        if end not in perms:
            ret.append((end, rule))
    return ret

