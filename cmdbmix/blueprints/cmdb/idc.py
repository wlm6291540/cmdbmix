from flask import request, render_template, redirect, url_for
from flask.blueprints import Blueprint
from flask_login import current_user, login_required

from cmdbmix.forms.cmdb import IdcAddForm, IdcEditForm
from cmdbmix.models.cmdb import Idc
from cmdbmix.utils import load_data_to_model, get_page_args, load_data_to_form

idc_bp = Blueprint('idc', __name__)


@idc_bp.route('/idc_manager', methods=['GET'])
@login_required
def idc_manager():
    page, per_page = get_page_args(request)
    pagination = Idc.query.paginate(page, per_page=per_page)
    return render_template('cmdb/idc.html', pagination=pagination)



@idc_bp.route('/idc_manager/add_idc', methods=['GET', 'POST'])
@login_required
def add_idc():
    form = IdcAddForm()
    if form.validate_on_submit():
        idc = Idc()
        load_data_to_model(idc, form).save()
        return redirect(url_for('idc.idc_manager'))
    return render_template('cmdb/add_idc.html', form=form)


@idc_bp.route('/idc_manager/edit_idc/<int:idc_id>', methods=['GET', 'POST'])
@login_required
def edit_idc(idc_id):
    form = IdcEditForm()
    idc = Idc.query.get_or_404(idc_id)
    if form.validate_on_submit():
        load_data_to_model(idc, form).save()
        return redirect(url_for('idc.idc_manager'))
    load_data_to_form(idc, form)
    return render_template('cmdb/edit_idc.html', form=form, idc=idc)


@idc_bp.route('/idc_manager/delete_idc/<int:idc_id>', methods=['GET', 'POST'])
@login_required
def delete_idc(idc_id):
    Idc.query.get_or_404(idc_id).delete()
    return redirect(url_for('idc.idc_manager'))