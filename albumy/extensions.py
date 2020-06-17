#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
    @Time    : 2020/6/14 10:29
    @Author  : Bright Hsu
    @Email   : hsubright@163.com
    @FileName: extensions.py
    @Software: PyCharm
"""


from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_wtf import CSRFProtect


db = SQLAlchemy()
moment = Moment()
csrf = CSRFProtect()
mail = Mail()
bootstrap = Bootstrap()
login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    from albumy.models import User
    user = User.query.get(int(user_id))
    return user


login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'warning'
login_manager.refresh_view = ''
login_manager.needs_refresh_message_category = 'warning'
