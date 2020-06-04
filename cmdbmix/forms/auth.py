from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField, SelectField
from wtforms.validators import DataRequired, ValidationError, Length

from cmdbmix.models.auth import Role, Permission, User

type_choices = [('页面', '页面'), ('操作', '操作'), ('页面和操作', '页面和操作')]


class LoginForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    remember = BooleanField("remember", default=False)
    submit = SubmitField()


class UserEditForm(FlaskForm):
    username = StringField(label="用户名", validators=[DataRequired()])
    nickname = StringField(label="昵称")
    email = StringField(label="邮箱", validators=[DataRequired()])
    is_active = BooleanField(label="状态")
    role_id = SelectField(label="角色", coerce=int)
    password = PasswordField(label="密码")
    submit = SubmitField()

    def validate_email(self, field):
        if User.query.filter(User.email==field.data).filter(User.username != self.username.data).all():
            raise ValidationError('邮箱已存在')

    def validate_password(self, field):
        if field.data is not '' and len(field.data) < 6:
            raise ValidationError("密码长度小于6位")


class UserAddForm(FlaskForm):
    username = StringField(label="用户名", validators=[DataRequired()])
    nickname = StringField(label="昵称")
    email = StringField(label="邮箱", validators=[DataRequired()])
    is_active = BooleanField(label="状态")
    role_id = SelectField(label="角色")
    password = PasswordField(label="密码", validators=[Length(6, 12)])
    submit = SubmitField()

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).all():
            raise ValidationError('邮箱已存在')


class PermEditForm(FlaskForm):
    name = StringField(label='权限名', validators=[DataRequired()])
    url = SelectField(label='URL', validators=[DataRequired()])
    type = SelectField(label='类型', validators=[DataRequired()], choices=type_choices)
    desc = TextAreaField(label='备注')
    submit = SubmitField()

    def validate_name(self, field):
        if Permission.query.filter(Permission.name==field.data and Permission.url == field.url).all():
            raise ValidationError('权限名已存在')


class PermAddForm(FlaskForm):
    name = StringField(label='权限名', validators=[DataRequired()])
    url = SelectField(label='URL', validators=[DataRequired()])
    type = SelectField(label='类型', validators=[DataRequired()], choices=type_choices)
    role = SelectField(label='角色')
    desc = TextAreaField(label='备注')
    submit = SubmitField()

    def validate_name(self, field):
        if len(Permission.query.filter(Permission.name==field.data).all()) > 1:
            raise ValidationError('权限名已存在')




class RoleEditForm(FlaskForm):
    name = StringField(label="角色名", validators=[DataRequired()])
    desc = TextAreaField(label='备注')
    submit = SubmitField()

    def validate_name(self, field):
        if len(Role.query.filter(Role.name==field.data).all()) > 1:
            raise ValidationError('角色名已存在')