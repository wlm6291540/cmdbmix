import hashlib

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from cmdbmix.extension import db

class BaseModel:
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()


class User(UserMixin, db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    nickname = db.Column(db.String(32))
    password_hash = db.Column(db.String(255))
    email = db.Column(db.String(64), unique=True, index=True)
    gravatar = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    role = db.relationship("Role", back_populates='users')

    def __init__(self):
        super(User).__init__()
        if self.email:
            self.gravatar = 'http://www.gravatar.com/avatar/%s?d=identicon' % self.email_hash


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def email_hash(self):
        return hashlib.md5(self.email.encode('utf-8')).hexdigest().lower()

    def generate_avatar(self):
        if self.email:
            self.gravatar = 'http://www.gravatar.com/avatar/%s?d=identicon' % self.email_hash

    def can(self, endpoint):
        if Permission.query.filter_by(url=endpoint).first() in self.role.permissions:
            return True
        else:
            return False


role_permission = db.Table('role_permission',
                           db.Column('role_id', db.Integer, db.ForeignKey('role.id')),
                           db.Column('permission_id', db.Integer, db.ForeignKey('permission.id')))

class Role(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    desc = db.Column(db.String(255))
    users = db.relationship('User', back_populates='role')
    permissions = db.relationship('Permission', secondary=role_permission, back_populates='roles')


class Permission(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    url = db.Column(db.String(255))
    type = db.Column(db.String(32))
    desc = db.Column(db.String(255))
    roles = db.relationship('Role', secondary=role_permission, back_populates='permissions')
