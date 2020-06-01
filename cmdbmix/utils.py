def format_form_errors(form):
    for name, error in form.errors.items():
        form.errors[name] = '\n'.join(*error)
    return form.errors