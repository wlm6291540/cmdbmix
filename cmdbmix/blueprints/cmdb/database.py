from flask import request, render_template, redirect, url_for
from flask.blueprints import Blueprint
from flask_login import login_required

from cmdbmix.forms.cmdb import DatabaseAddForm, DatabaseEditForm
from cmdbmix.models.cmdb import Database, Host, Tag
from cmdbmix.utils import get_page_args, load_data_to_model, load_data_to_form

db_bp = Blueprint('db', __name__)


@db_bp.route('/db_manager', methods=['GET'])
@login_required
def db_manager():
    page, per_page = get_page_args(request)
    pagination = Database.query.paginate(page, per_page=per_page)
    return render_template('cmdb/database.html', pagination=pagination)


@db_bp.route('/db_manager/add_db', methods=['GET', 'POST'])
@login_required
def add_db():
    form = DatabaseAddForm()
    form.tag_id.choices = [(tag.id, tag.name) for tag in Tag.query.all()]
    form.host_id.choices = [(host.id, host.hostname) for host in Host.query.all()]
    if form.validate_on_submit():
        db = Database()
        db = load_data_to_model(db, form)
        db.save()
        return redirect(url_for('db.db_manager'))
    print(form.errors)
    return render_template('cmdb/add_db.html', form=form)


@db_bp.route('/db_manager/edit_db/<int:db_id>', methods=['GET', 'POST'])
@login_required
def edit_db(db_id):
    form = DatabaseEditForm()
    form.tag_id.choices = [(tag.id, tag.name) for tag in Tag.query.all()]
    form.host_id.choices = [(host.id, host.hostname) for host in Host.query.all()]
    db = Database.query.get_or_404(db_id)
    if form.validate_on_submit():
        load_data_to_model(db, form).save()
        return redirect(url_for('db.db_manager'))
    form = load_data_to_form(db, form)
    form.tag_id.data = db.tag_id
    form.host_id.data = db.host_id
    return render_template('cmdb/edit_db.html', form=form, db=db)

@db_bp.route('/db_manager/delete_db/<int:db_id>', methods=['GET', 'POST'])
@login_required
def delete_db(db_id):
    Database.query.get_or_404(db_id).delete()
    return redirect(url_for('db.db_manager'))