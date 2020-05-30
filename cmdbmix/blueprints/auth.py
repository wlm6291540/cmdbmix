from flask import request, render_template, redirect, url_for
from flask.blueprints import Blueprint
from flask_login import current_user, login_user, logout_user, login_required

from cmdbmix.models.auth import User
from cmdbmix.forms.auth import LoginForm

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            user = User.query.filter_by(username=username).first()
            print(user)
            if user.validate_password(password):
                login_user(user)
                return redirect(url_for('main.home'))
            else:
                return render_template('auth/login.html', form=form, message='密码错误')
    return render_template('auth/login.html', form=form)



@auth_bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))



@auth_bp.route('/forget_password', methods=['GET', 'POST'])
def forget_password():
    return render_template('auth/forgot-password.html')


