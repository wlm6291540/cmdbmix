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