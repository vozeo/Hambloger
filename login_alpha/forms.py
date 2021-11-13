"""
    定义了网站需要的表单
"""

# 这些模块提供了flask表单支持
# 参考文档：http://www.pythondoc.com/flask-wtf/
from flask_wtf import FlaskForm
from flask_wtf.recaptcha.fields import RecaptchaField
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, DateTimeField, SelectField
from wtforms.fields.core import IntegerField, TimeField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError

CONST_NICK_LENGTH_MIN = 8
CONST_NICK_LENGTH_MAX = 25
CONST_PASW_LENGTH_MIN = 8
CONST_PASW_LENGTH_MAX = 30

# 自定义规则
class UserNickRule(object):
    def __init__(self, inst_log=None, length_log=None, context_log=None):
        self.inst_log = inst_log
        self.length_log = length_log
        self.context_log = context_log
    
    def __call__(self, form, field):
        data = field.data
        # 用户名域为空或类型不合法
        if data is None or not isinstance(data, str):
            log = self.inst_log
            if log is None or not isinstance(log, str):
                log = 'UserNickRule validation failed: unresolved type or none'
        # 长度超限
        elif len(data) < CONST_NICK_LENGTH_MIN or len(data) > CONST_NICK_LENGTH_MAX:
            log = self.length_log
            if log is None or not isinstance(log, str):
                log = 'UserNickRule validation failed: length %d out of range(%d, %d)' % (len(data), 
                    CONST_NICK_LENGTH_MIN, CONST_NICK_LENGTH_MAX + 1
                )
            raise ValidationError(log)
        else:
            for ch in data:
                ch_asc = ord(ch)
                # ascii非法判断
                if not (ch_asc >= 0x41 and ch_asc <= 0x5a) and not (ch_asc >= 0x61 and ch_asc <= 0x7f) and \
                    not (ch_asc >= 0x30 and ch_asc <= 0x39) and not (ch_asc == 0x5f): 
                    log = self.context_log
                    if log is None or not isinstance(log, str):
                        log = 'UserNickRule validation failed: illegal character(%s)' % ch
                    raise ValidationError(log)

class UserPasswordRule(object):
    def __init__(self, inst_log=None, length_log=None, context_log=None):
        self.inst_log = inst_log
        self.length_log = length_log
        self.context_log = context_log
    
    def __call__(self, form, field):
        data = field.data
        # 密码域为空或类型不合法
        if data is None or not isinstance(data, str):
            log = self.inst_log
            if log is None or not isinstance(log, str):
                log = 'UserPasswordRule validation failed: unresolved type or none'
            raise ValidationError(log)
        # 密码长度非法
        elif len(data) < CONST_PASW_LENGTH_MIN or len(data) > CONST_PASW_LENGTH_MAX:
            log = self.length_log
            if log is None or not isinstance(log, str):
                log = 'UserPasswordRule validation failed: length %d out of range(%d, %d)' % (len(data), 
                    CONST_PASW_LENGTH_MIN, CONST_PASW_LENGTH_MAX + 1
                )
            raise ValidationError(log)
        # 检查字符类型：必须出现两类以上（字母，数字，符号），不能有非法字符
        else:
            exist_alpha, exist_num, exist_sign = False, False, False
            for ch in data:
                ch_asc = ord(ch)
                if (ch_asc >= 0x41 and ch_asc <= 0x5a) or (ch_asc >= 0x61 and ch_asc <= 0x7f):
                    exist_alpha = True
                elif (ch_asc >= 0x30 and ch_asc <= 0x39):
                    exist_num = True
                elif (ch_asc >= 0x20 and ch_asc <= 0x7e):
                    exist_sign = True
                else:
                    log = self.context_log
                    if log is None or not isinstance(log, str):
                        log = 'UserPasswordRule validation failed: illegal character(%s)' % (ch)
                    raise ValidationError(log)
            if int(exist_alpha) + int(exist_num) + int(exist_sign) < 2:
                log = self.context_log
                if log is None or not isinstance(log, str):
                    log = 'UserPasswordRule validation failed: at least two character classes required, \
                        alpha=%s, num=%s, sign=%s' % (str(exist_alpha), str(exist_num), str(exist_sign))
                raise ValidationError(log)

# 主页上的登录键
class LoginKey(FlaskForm):
    submit1 = SubmitField('Sign In')

# 主页上的注册键
class RegisterKey(FlaskForm):
    submit2 = SubmitField('Sign Up')

# 主页上的登出键
class LogoutKey(FlaskForm):
    submit3 = SubmitField('Sign Out')

# 登录页表单
class LoginForm(FlaskForm):
    nick = StringField('ID', validators=[DataRequired(), Length(CONST_NICK_LENGTH_MIN, CONST_NICK_LENGTH_MAX)])
    key = PasswordField('Password', validators=[DataRequired(), Length(CONST_PASW_LENGTH_MIN, CONST_PASW_LENGTH_MAX)])
    submit = SubmitField('Login!')

# 注册页表单
class RegisterForm(FlaskForm):
    nick = StringField('Enter ID', validators=[
        DataRequired(), 
        Length(CONST_NICK_LENGTH_MIN, CONST_NICK_LENGTH_MAX),
        UserNickRule()
        ])
    type = IntegerField('Enter Account Rank', validators=[DataRequired(), NumberRange(-1, 4)])
    key = PasswordField('Enter Password', validators=[
        DataRequired(), 
        Length(CONST_PASW_LENGTH_MIN, CONST_PASW_LENGTH_MAX),
        UserPasswordRule()
        ])
    keyc = PasswordField('Confirm Password', validators=[
        DataRequired(), 
        Length(CONST_PASW_LENGTH_MIN, CONST_PASW_LENGTH_MAX),
        UserPasswordRule()
        ])
    submit = SubmitField('Register!')
