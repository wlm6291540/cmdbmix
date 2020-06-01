from flask import request, render_template, redirect, url_for
from flask.blueprints import Blueprint
from flask_login import current_user, login_user, logout_user, login_required

from cmdbmix.models.auth import User, Permission
from cmdbmix.forms.auth import LoginForm, PermEditForm

perm_bp = Blueprint('perm', __name__)


@perm_bp.route('/perm_manager', methods=['GET'])
@login_required
def perm_manager():
    perms = Permission.query.all()
    return render_template('perms/perm.html', perms=perms)



@perm_bp.route('/perm_manager/edit_perm/<int:perm_id>', methods=['GET'])
@login_required
def edit_perm(perm_id):
    perm = Permission.query.get_or_404(perm_id)
    form = PermEditForm()
    if form.validate_on_submit():
        perm.name = form.name.data
        perm.url = form.url.data
        perm.type = form.type.data
        perm.desc = form.desc.data
        perm.save()
        return redirect(url_for('perm.perm_manager'))
    return render_template('perms/edit_perm.html', perm=perm, form=form)

