from flask import request, render_template, redirect, url_for
from flask.blueprints import Blueprint
from flask_login import current_user, login_required

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
@login_required
def home():
    if current_user.is_authenticated:
        return render_template('home.html')
    return redirect(url_for('auth.login'))



@main_bp.route('/about', methods=['GET'])
@login_required
def about():
    return render_template('home.html')
