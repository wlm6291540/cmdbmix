from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SelectField, TextAreaField, HiddenField, DateTimeField
from wtforms.validators import DataRequired, ValidationError

from cmdbmix.models.cmdb import Idc

tag_type_choices = [('host', '主机'), ('database', '数据库')]
class TagForm(FlaskForm):
    name = StringField(label='标签名', validators=[DataRequired()])
    type = SelectField(label='类型', choices=tag_type_choices, validators=[DataRequired()])
    desc = TextAreaField(label='备注')


idc_area_choices = [('本地', '本地'), ('阿里云', '阿里云'), ('百度云', '百度云'), ('华为云', '华为云')]
class IdcAddForm(FlaskForm):
    name = StringField(label='idc名', validators=[DataRequired()])
    area = SelectField(label='区域', choices=idc_area_choices)
    desc = TextAreaField(label='备注')

    def validate_name(self, field):
        if Idc.query.filter_by(name=field.data).first():
            raise ValidationError('{} 已存在'.format(field.data))


class IdcEditForm(FlaskForm):
    id = HiddenField(validators=[DataRequired()])
    name = StringField(label='idc名', validators=[DataRequired()])
    area = SelectField(label='区域', choices=idc_area_choices)
    desc = TextAreaField(label='备注')



class ServerAddForm(FlaskForm):
    name = StringField(label='服务器', validators=[DataRequired()])
    manager_ip = StringField(label='管理Ip')
    public_ip = StringField(label='公网Ip')
    private_ip = StringField(label='私网Ip')
    idc = SelectField(label='IDC')
    desc = TextAreaField(label='备注')


class ServerEditForm(FlaskForm):
    id = HiddenField(validators=[DataRequired()])
    name = StringField(label='服务器', validators=[DataRequired()])
    manager_ip = StringField(label='管理Ip')
    public_ip = StringField(label='公网Ip')
    private_ip = StringField(label='私网Ip')
    idc_id = SelectField(label='IDC', coerce=int)
    desc = TextAreaField(label='备注')




host_stat_choices = [('已停止', '已停止'), ('已禁用','已禁用',), ('已到期', '已到期'), ('正常', '正常')]
class HostAddForm(FlaskForm):
    hostname = StringField(label='主机名', validators=[DataRequired()])
    public_ip = StringField(label='公网Ip')
    private_ip = StringField(label='私网Ip')
    status = SelectField(label='状态', default='正常', choices=host_stat_choices)
    tag_id = SelectField(label='标签', coerce=int)
    server_id = SelectField(label='服务器', coerce=int)
    create_time = DateTimeField(label='创建时间')
    expire_time = DateTimeField(label='过期时间')
    desc = TextAreaField(label='备注')



class HostEditForm(FlaskForm):
    id = HiddenField(validators=[DataRequired()])
    hostname = StringField(label='主机名', validators=[DataRequired()])
    public_ip = StringField(label='公网Ip')
    private_ip = StringField(label='私网Ip')
    status = SelectField(label='状态', default='正常', choices=host_stat_choices)
    tag_id = SelectField(label='IDC', coerce=int)
    server_id = SelectField(label='服务器', coerce=int)
    create_time = DateTimeField(label='创建时间')
    expire_time = DateTimeField(label='过期时间')
    desc = TextAreaField(label='备注')
