from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect



db = SQLAlchemy()
csrf = CSRFProtect()
login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    from cmdbmix.models.auth import User
    return User.query.get_or_404(user_id)

login_manager.login_view = 'auth.login'