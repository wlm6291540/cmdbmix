import paramiko


def format_form_errors(form):
    for name, error in form.errors.items():
        form.errors[name] = '\n'.join(*error)
    return form.errors


def perm_to_list(perms):
    ret = []
    for perm in perms:
        ret.append([
            perm.id, perm.name, perm.url, perm.type, perm.desc
        ])
    return ret


def get_page_args(request):
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=10)
    return page, per_page


def load_data_to_model(model, form, except_fields=[]):
    for name, field in form._fields.items():
        if name not in except_fields and name != 'csrf_token':
            if field.data is not None:
                setattr(model, name, field.data)
    return model


def load_data_to_form(model, form, except_fields=[]):
    for name, field in form._fields.items():
        if name not in except_fields and name != 'csrf_token':
            value = getattr(model, name)
            setattr(form._fields[name], 'data', value)
    return form


def connect_host(ip, port, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=ip, port='22', username=username, password=password)
    return client
