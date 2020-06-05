from datetime import datetime

from cmdbmix import db
from cmdbmix.models.utils import BaseModel


class Tag(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    type = db.Column(db.String(32), comment='类型: host, database')
    desc = db.Column(db.String(255))
    hosts = db.relationship('Host', back_populates='tag')
    databases = db.relationship('Database', back_populates='tag')


class Idc(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    area = db.Column(db.String(255))
    desc = db.Column(db.String(255))
    servers = db.relationship('Server', back_populates='idc')


class Server(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    manager_ip = db.Column(db.String(64))
    public_ip = db.Column(db.String(64))
    private_ip = db.Column(db.String(64))
    idc_id = db.Column(db.Integer, db.ForeignKey('idc.id'))
    idc = db.relationship('Idc', back_populates='servers')
    desc = db.Column(db.String(255))
    hosts = db.relationship('Host', backref='server')
    create_time = db.Column(db.DateTime, default=datetime.utcnow(), comment='上架时间')


class Host(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    hostname = db.Column(db.String(64))
    public_ip = db.Column(db.String(64))
    private_ip = db.Column(db.String(64))
    status = db.Column(db.String(64), comment='状态: 已停止, 已禁用, 已到期, 正常')
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))
    tag = db.relationship('Tag', back_populates='hosts')
    server_id = db.Column(db.Integer, db.ForeignKey('server.id'))
    desc = db.Column(db.String(255), comment='备注')
    create_time = db.Column(db.DateTime, default=datetime.utcnow(), comment='创建时间')
    expire_time = db.Column(db.DateTime, default='', comment='过期时间')


class Database(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    version = db.Column(db.String(64))
    public_ip = db.Column(db.String(255))
    private_ip = db.Column(db.String(255))
    host_id = db.Column(db.Integer, db.ForeignKey('host.id'))
    host = db.relationship('Host', uselist=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))
    tag = db.relationship('Tag', back_populates='databases')
    create_time = db.Column(db.DateTime, default=datetime.utcnow(), comment='创建时间')
    expire_time = db.Column(db.DateTime, default='', comment='过期时间')