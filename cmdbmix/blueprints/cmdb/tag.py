from flask import request, render_template, redirect, url_for
from flask.blueprints import Blueprint
from flask_login import current_user, login_user, logout_user, login_required

from cmdbmix.forms.cmdb import TagForm
from cmdbmix.models.cmdb import Tag
from cmdbmix.utils import get_page_args, load_data_to_model, load_data_to_form

tag_bp = Blueprint('tag', __name__)


@tag_bp.route('/tag_manager', methods=['GET'])
@login_required
def tag_manager():
    page, per_page = get_page_args(request)
    pagination = Tag.query.paginate(page, per_page=per_page)
    return render_template('cmdb/tag.html', pagination=pagination)


@tag_bp.route('/tag_manager/add_tag', methods=['GET', 'POST'])
@login_required
def add_tag():
    form = TagForm()
    if form.validate_on_submit():
        tag = Tag()
        load_data_to_model(tag, form)
        tag.save()
        return redirect(url_for('tag.tag_manager'))
    return render_template('cmdb/add_tag.html', form=form)


@tag_bp.route('/tag_manager/delete_tag/<int:tag_id>', methods=['GET'])
@login_required
def delete_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    tag.delete()
    return redirect(url_for('tag.tag_manager'))


@tag_bp.route('/tag_manager/edit_tag/<int:tag_id>', methods=['GET', 'POST'])
@login_required
def edit_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    form = TagForm()
    if form.validate_on_submit():
        tag = load_data_to_model(tag, form)
        tag.save()
        return redirect(url_for('tag.tag_manager'))
    form = load_data_to_form(tag, form)
    return render_template('cmdb/edit_tag.html', form=form, tag=tag)




