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
from flask_login import current_user, logout_user, login_user, login_required
from flask import redirect, url_for, render_template, flash
from albumy.forms.auth import RegisterForm, LoginFrom, ForgetPasswordForm, ResetPassword
from albumy.models import User
from albumy.extensions import db
from albumy.settings import Operations
from albumy.utils import generate_token, redirect_back, validate_token
from albumy.emails import send_confirm_email, send_reset_password_email


auth_bp = Blueprint('auth', __name__)


# 用户登录视图
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # 如果当前用户已经登录 重定向到主页
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginFrom()
    if form.validate_on_submit():
        # 根基表单提供的email 查询到数据库对应的用户对象
        user = User.query.filter_by(email=form.email.data.lower()).first()
        # 验证 用户存在与否 且 验证密码正确与否
        if user is not None and user.validate_password(form.password.data):
            if login_user(user, form.remember.data):
                flash('Login success.', 'info')
                return redirect_back()
            else:
                flash('Your account is blocked.', 'warning')
                return redirect(url_for('main.index'))
        flash('Invalid email or password.', 'waring')
    return render_template('auth/login.html', form=form)


# 用户注册视图
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    # 当前用户已登录 重定向到主页
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
        # 生成用户邮箱验证令牌
        token = generate_token(user=user, operation=Operations.CONFIRM)
        # 发送令牌到用户邮箱
        send_confirm_email(user=user, token=token)
        flash('Confirm email sent, check your inbox.', 'info')
        return redirect(url_for('.login'))
    return render_template('auth/register.html', form=form)


# 验证令牌试图 只能是登录用户才能访问-视图保护
@auth_bp.route('/confirm/<token>')
@login_required
def confirm(token):
    # 如果当前用户已通过验证 重定向到主页
    if current_user.confirmed:
        return redirect(url_for('main.index'))

    # 令牌验证
    if validate_token(user=current_user, token=token, operation=Operations.CONFIRM):
        flash('Account confirm.', 'success')
        return redirect(url_for('main.index'))
    else:
        flash('Invalid or expired token.', 'danger')
        return redirect(url_for('.resend_confirmation'))


# 重新发送验证令牌 消息, 只能是登录用户才能访问-视图保护
@auth_bp.route('/resend-confirm-email')
@login_required
def resend_confirm_email():
    # 当前用户已经通过验证 重定向到主页
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    # 重新生产验证令牌信息
    token = generate_token(user=current_user, operation=Operations.CONFIRM)
    # 发送到当前用户的邮箱
    send_confirm_email(user=current_user, token=token)
    flash('New email sent, check your inbox.', 'info')
    return redirect(url_for('main.index'))


# 用户忘记密码视图
@auth_bp.route('/forget-password', methods=['GET', 'POST'])
def forget_password():
    # 当前用户已经登录 重定向到主页
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = ForgetPasswordForm()
    if form.validate_on_submit():
        # 数据库中查询 表单所对应的邮箱，返回用户对象
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user:
            # 生成令牌并发送到邮箱
            token = generate_token(user=user, operation=Operations.RESET_PASSWORD)
            send_reset_password_email(user=user, token=token)
            flash('Password reset email sent, check you inbox.', 'info')
            return redirect(url_for('.login'))
        flash('Invalid email.', 'warning')
        return redirect(url_for('.forget_password'))
    return render_template('auth/forget_password.html', form=form)


# 密码修改视图
@auth_bp.route('/reset/password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    # 当前用户已经登录 重定向到主页
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = ResetPassword()
    if form.validate_on_submit():
        # 数据库中查询 表单所对应的邮箱，返回用户对象
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user is None:
            return redirect(url_for('main.index'))
        # 验证令牌 并传入表单提供的新密码
        if validate_token(user=user, token=token, operation=Operations.RESET_PASSWORD,
                          new_password=form.password.data):
            flash('Password updated.', 'success')
            return redirect(url_for('.login'))
        else:
            flash('Invalid or expired token.', 'danger')
            return redirect(url_for('.forget_password'))

    return render_template('auth/reset_password.html', form=form)


@auth_bp.route('logout')
@login_required
def logout():
    logout_user()
    flash('Logout success.', 'info')
    return redirect(url_for('main.index'))