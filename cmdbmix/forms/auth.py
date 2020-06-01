from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, ValidationError, Length

from cmdbmix.models.auth import Role, Permission


class LoginForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    remember = BooleanField("remember", default=False)
    submit = SubmitField()


class UserEditForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    nickname = StringField("nickname")
    email = StringField("email", validators=[DataRequired()])
    is_active = BooleanField('is_active')
    role_id = IntegerField('role_id')
    password = PasswordField("password", validators=[Length(6, 12)])
    submit = SubmitField()


class PermEditForm(FlaskForm):
    name = StringField("name", validators=[DataRequired()])
    url = StringField("url", validators=[DataRequired()])
    type = StringField("type", validators=[DataRequired()])
    desc = TextAreaField('desc')
    submit = SubmitField()

    def validate_name(self, field):
        if Permission.query.filter(Permission.name==field.data).all():
            raise ValidationError('权限名已存在')




class RoleEditForm(FlaskForm):
    name = StringField("name", validators=[DataRequired()])
    desc = TextAreaField('desc')
    submit = SubmitField()

    def validate_name(self, field):
        if Role.query.filter(Role.name==field.data).all():
            raise ValidationError('角色名已存在')