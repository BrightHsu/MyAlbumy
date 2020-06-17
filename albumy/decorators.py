#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
    @Time    : 2020/6/14 10:40
    @Author  : Bright Hsu
    @Email   : hsubright@163.com
    @FileName: decorators.py
    @Software: PyCharm
"""


from functools import wraps


from flask import Markup, flash, url_for, redirect
from flask_login import current_user


# 过滤未确定用户的装饰器
# Markup类 可以将文本标记为安全文本，避免渲染时转义
def confirm_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.confirmed:
            message = Markup(
                'Please confirm your account first.'
                'Not receive the email?'
                '<a class="alert-link" href="%s">Resend Confirm Email</a>' %
                url_for('auth.resend_confirm_email'))
            flash(message, 'waring')
            return redirect(url_for('main.index'))
        return func(*args, **kwargs)
    return decorated_function
