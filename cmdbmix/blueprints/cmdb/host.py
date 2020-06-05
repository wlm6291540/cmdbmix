from flask import request, render_template, redirect, url_for, g, jsonify
from flask.blueprints import Blueprint
from flask_login import current_user, login_required
from flask_socketio import emit

from cmdbmix.extension import socketio, clients_map
from cmdbmix.forms.cmdb import HostAddForm, HostEditForm
from cmdbmix.models.cmdb import Host, Tag, Server
from cmdbmix.utils import load_data_to_form, load_data_to_model, get_page_args, connect_host

host_bp = Blueprint('host', __name__)


@host_bp.route('/host_manager', methods=['GET'])
@login_required
def host_manager():
    page, per_page = get_page_args(request)
    pagination = Host.query.paginate(page, per_page=per_page)
    return render_template('cmdb/host.html', pagination=pagination)




@host_bp.route('/host_manager/add_host', methods=['GET', 'POST'])
@login_required
def add_host():
    form = HostAddForm()
    form.tag_id.choices = [(tag.id, tag.name) for tag in Tag.query.all()]
    form.server_id.choices = [(server.id, server.name) for server in Server.query.all()]
    if form.validate_on_submit():
        host = Host()
        host = load_data_to_model(host, form, except_fields=[''])
        host.save()
        return redirect(url_for('host.host_manager'))
    return render_template('cmdb/add_host.html', form=form)


@host_bp.route('/host_manager/edit_host/<int:host_id>', methods=['GET', 'POST'])
@login_required
def edit_host(host_id):
    form = HostEditForm()
    host = Host.query.get_or_404(host_id)
    form.tag_id.choices = [(tag.id, tag.name) for tag in Tag.query.all()]
    form.server_id.choices = [(server.id, server.name) for server in Server.query.all()]
    if form.validate_on_submit():
        load_data_to_model(host, form).save()
        return redirect(url_for('host.host_manager'))
    form = load_data_to_form(host, form)
    form.tag_id.data = host.tag_id
    form.server_id.data = host.server_id
    return render_template('cmdb/edit_host.html', form=form, host=host)

@host_bp.route('/host_manager/delete_host/<int:host_id>', methods=['GET', 'POST'])
@login_required
def delete_host(host_id):
    Host.query.get_or_404(host_id).delete()
    return redirect(url_for('host.host_manager'))


@host_bp.route('/host_manager/web_ssh/<int:host_id>', methods=['GET', 'POST'])
@login_required
def web_ssh(host_id):
    host = Host.query.get_or_404(host_id)
    return render_template('cmdb/web_ssh.html', host=host)


@host_bp.route('/host_manager/connect', methods=['GET', 'POST'])
@login_required
def connect():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
        ip, username, password = data['ip'], data['username'], data['password']
        print(ip)
        if ip in clients_map:
            client = clients_map[ip]
        else:
            client = connect_host(ip, 22, username, password)
        if client:
            clients_map[data['ip']] = client
            return jsonify({
                'status': '连接成功'
            })
    return jsonify({
        'status': '连接失败'
    }), 400


@host_bp.route('/host_manager/close_connect', methods=['GET', 'POST'])
@login_required
def close_connect():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
        ip = data['ip']
        if clients_map.get(ip, None):
            client = clients_map[ip]
            client.close()
            clients_map.pop(ip)
            return jsonify({
                'msg': '已关闭'
            })
    return jsonify({
        'msg': '关闭失败'
    }), 400


@socketio.on('connect', namespace='/')
def connect():
    print('connected')
    pass

@socketio.on('new command', namespace='/')
def new_command(command):
    ip, cmd = command['ip'], command['command'][0:-1]
    client = clients_map.get(ip, None)
    if client:
        _, stdout, stderr = client.exec_command(cmd)
        stdout, stderr = stdout.read().decode('utf8'), stderr.read().decode('utf8')
        result = ''
        if stdout:
            result = stdout
        if stderr:
            result = stderr
        emit('new command', {
            'code': 0,
            'msg': '执行成功',
            'result': result.replace("\n", "\r\n")
        })
    else:
        emit('new command', {
            'code': 2,
            'msg': '连接已失效',
            'result': ""
        })
