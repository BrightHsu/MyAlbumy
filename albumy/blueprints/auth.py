#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
    @Time    : 2020/6/14 10:42
    @Author  : Bright Hsu
    @Email   : hsubright@163.com
    @FileName: auth.py
    @Software: PyCharm
"""


from flask import Blueprint
from flask_login import current_user
from flask import redirect, url_for, render_template, flash
from albumy.forms.auth import RegisterForm
from albumy.models import User
from albumy.extensions import db


auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegisterForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data.lower()  # 小写处理
        username = form.username.data
        password = form.password.data
        user = User(name=name, email=email, username=username)
        user.set_password(password)  # 设置密码
        db.session.add(user)
        db.session.commit()
        # token = generate_token(user=user, operation=Op)
    return render_template('auth/register.html', form=form)
