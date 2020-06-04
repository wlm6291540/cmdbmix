import os

import click
from flask import Flask, g

from cmdbmix.extension import db, login_manager, csrf, socketio
from cmdbmix.setting import config
from cmdbmix.blueprints.auth import auth_bp
from cmdbmix.blueprints.main import main_bp
from cmdbmix.blueprints.perms.perm import perm_bp
from cmdbmix.blueprints.perms.role import role_bp
from cmdbmix.blueprints.perms.user import user_bp
from cmdbmix.blueprints.cmdb.host import host_bp
from cmdbmix.blueprints.cmdb.server import server_bp
from cmdbmix.blueprints.cmdb.database import db_bp
from cmdbmix.blueprints.cmdb.idc import idc_bp
from cmdbmix.blueprints.cmdb.tag import tag_bp



def create_app(env_name='development'):
    app = Flask('cmdbmix')
    sys_env = os.getenv('FLASK_ENV')
    if sys_env:
        app.config.from_object(config[sys_env])
    else:
        app.config.from_object(config[env_name])
    register_extensions(app)
    register_commands(app)
    register_blueprints(app)
    return app


def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(role_bp)
    app.register_blueprint(perm_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(host_bp)
    app.register_blueprint(server_bp)
    app.register_blueprint(db_bp)
    app.register_blueprint(idc_bp)
    app.register_blueprint(tag_bp)


def register_commands(app):
    @app.cli.command('init', help="Initialized database.")
    @click.option('--drop', is_flag=True, default=False, prompt='Are you sure to drop old database.')
    def init(drop):
        if drop:
            db.drop_all()
            click.echo('old database has dropped.')
        db.create_all()
        click.echo('database has initialized.')

    @app.cli.command('add_admin', help="Add a admin user")
    def add_admin():
        from cmdbmix.models.auth import User
        user = User()
        user.username = 'admin'
        user.email = 'wlm6291540@163.com'
        user.set_password('123456')
        user.generate_avatar()
        user.save()


def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(app)
    # csrf.init_app(app)