"""
    定义了网站数据库模型
    警告：对模型的任何修改都需要先备份数据库和原模型代码
"""

from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from login_alpha import db

class Users(db.Model, UserMixin):
    # 主键：有全局意义的ID
    id = db.Column(db.Integer, primary_key=True, index=True)
    nick = db.Column(db.String(25))
    # 密码：只储存哈希值
    key = db.Column(db.String(128))
    # 关联信息
    regis_date = db.Column(db.DateTime, default=datetime.utcnow) # 注册时间
    # 附加信息
    type = db.Column(db.Integer) # 账户类别

    def set_password(self, password):
        self.key = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.key, password)
