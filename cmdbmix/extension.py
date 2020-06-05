from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_socketio import SocketIO
from flask_migrate import Migrate



db = SQLAlchemy()
csrf = CSRFProtect()
login_manager = LoginManager()
socketio = SocketIO()
migrate = Migrate()

clients_map = {}

@login_manager.user_loader
def load_user(user_id):
    from cmdbmix.models.auth import User
    return User.query.get_or_404(user_id)

login_manager.login_view = 'auth.login'