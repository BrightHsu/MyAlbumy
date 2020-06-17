#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
    @Time    : 2020/6/14 10:28
    @Author  : Bright Hsu
    @Email   : hsubright@163.com
    @FileName: emails.py
    @Software: PyCharm
"""


from threading import Thread

from albumy.extensions import mail
from flask_mail import Message
from flask import current_app, render_template


def _send_async_mail(app, message):
    with app.app_context():
        mail.send(message)


def send_mail(subject, to, template, **kwargs):
    message = Message(subject=current_app.config['ALBUMY_MAIL_SUBJECT_PREFIX'] + subject, recipients=[to])
    message.body = render_template(template + '.txt', **kwargs)
    message.html = render_template(template + '. html', **kwargs)
    app = current_app._get_current_object()  # 获取被代理的真实对象
    thr = Thread(target=_send_async_mail, args=[app, message])
    thr.start()
    return thr


def send_confirm_email(user, token, to=None):
    send_mail(subject='Email Confirm', to=to or user.email, template='email/confirm', user=user, token=token)


def send_reset_password_email(user, token):
    send_mail(subject='Password Reset', to=user.email, template='email/reset_password', user=user, token=token)


def send_change_email_email(user, token, to=None):
    send_mail(subject='Change Email Confirm', to=to or user.email, template='emails/change_email', user=user, token=token)