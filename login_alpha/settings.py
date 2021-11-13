"""
    项目和数据库的一些有关配置
"""
import os
import sys

from login_alpha import app

# SQLite统一资源标识符前缀：在Win系统下为三斜杠
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

# 数据库文件目录
dev_db = prefix + os.path.join(os.path.dirname(app.root_path), 'data.db')

# 一些设置选项
SECRET_KEY = os.getenv('SECRET_KEY', 'secret string')
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', dev_db)