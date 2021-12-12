from flask_pagedown.fields import PageDownField
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.simple import FileField, TextAreaField
from wtforms.validators import DataRequired, Length
from flask_pagedown.fields import PageDownField
from flask_wtf.file import FileField, FileAllowed

class NameForm(FlaskForm):
    name = StringField("请输入您的用户名: ", validators=[DataRequired()])
    submit = SubmitField("登录")


class EditProfileForm(FlaskForm):
    mask = FileField('头像', validators=[
            FileAllowed(['png'])
        ])
    name = StringField('真实姓名', validators=[Length(0, 64)])
    location = StringField('地址', validators=[Length(0, 64)])
    about_me = StringField('个人简介', validators=[Length(0, 64)])
    submit = SubmitField('提交')


class PostForm(FlaskForm):
    title = StringField('标题', validators=[Length(0, 64)])
    sub_title = StringField('副标题', validators=[Length(0, 64)])
    body = PageDownField("要写点什么？", validators=[DataRequired()])
    submit = SubmitField('写完了')
