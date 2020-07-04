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
from flask_login import LoginManager, AnonymousUserMixin
from flask_wtf import CSRFProtect
from flask_dropzone import Dropzone
from flask_avatars import Avatars


db = SQLAlchemy()
moment = Moment()
csrf = CSRFProtect()
mail = Mail()
bootstrap = Bootstrap()
login_manager = LoginManager()
dropzone = Dropzone()
avatars = Avatars()


@login_manager.user_loader
def load_user(user_id):
    from albumy.models import User
    user = User.query.get(int(user_id))
    return user


login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'warning'
login_manager.refresh_view = ''
login_manager.needs_refresh_message_category = 'warning'


# 访客，匿名用户
# 当访客浏览网站时，程序中的current_user将指向这个Guest类的实例
# 因为访客不具有任何已经定义的权限，更不可能是管理员，
# 所有can（）方法和is_admin属性均直接返回False
class Guest(AnonymousUserMixin):
    @property
    def is_admin(self):
        return False

    def can(self, permission_name):
        return False


login_manager.anonymous_user = Guest

