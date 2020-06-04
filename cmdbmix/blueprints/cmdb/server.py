from flask import request, render_template, redirect, url_for
from flask.blueprints import Blueprint
from flask_login import login_required

from cmdbmix.decorators import auth_required
from cmdbmix.forms.cmdb import ServerAddForm, ServerEditForm
from cmdbmix.models.cmdb import Server, Idc
from cmdbmix.utils import get_page_args, load_data_to_model, load_data_to_form

server_bp = Blueprint('server', __name__)


@server_bp.route('/server_manager', methods=['GET'])
@login_required
def server_manager():
    page, per_page = get_page_args(request)
    pagination = Server.query.paginate(page, per_page=per_page)
    return render_template('cmdb/server.html', pagination=pagination)



@server_bp.route('/server_manager/add_server', methods=['GET', 'POST'])
@login_required
def add_server():
    form = ServerAddForm()
    form.idc.choices = [(str(idc.id), idc.name) for idc in Idc.query.all()]
    if form.validate_on_submit():
        server = Server()
        server = load_data_to_model(server, form, except_fields=['idc'])
        server.idc = Idc.query.get_or_404(form.idc.data)
        server.save()
        return redirect(url_for('server.server_manager'))
    return render_template('cmdb/add_server.html', form=form)


@server_bp.route('/server_manager/edit_server/<int:server_id>', methods=['GET', 'POST'])
@login_required
def edit_server(server_id):
    form = ServerEditForm()
    form.idc_id.choices = [(idc.id, idc.name) for idc in Idc.query.all()]
    server = Server.query.get_or_404(server_id)
    if form.validate_on_submit():
        load_data_to_model(server, form).save()
        return redirect(url_for('server.server_manager'))
    form = load_data_to_form(server, form)
    form.idc_id.data = server.idc_id
    return render_template('cmdb/edit_server.html', form=form, server=server)

@server_bp.route('/server_manager/delete_server/<int:server_id>', methods=['GET', 'POST'])
@login_required
def delete_server(server_id):
    Server.query.get_or_404(server_id)
    return redirect(url_for('server.server_manager'))