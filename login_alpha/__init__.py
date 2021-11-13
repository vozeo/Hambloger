"""
    测试网站模块初始化
"""
import os
import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

app = Flask('login_alpha')

# SQLite统一资源标识符前缀：在Win系统下为三斜杠
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

# 数据库文件目录
dev_db = prefix + os.path.join(os.path.dirname(app.root_path), 'data.db')

# 一些设置选项
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'secret string')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', dev_db)

db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
logm = LoginManager(app)

from login_alpha import views