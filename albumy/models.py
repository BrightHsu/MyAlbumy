#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
    @Time    : 2020/6/14 10:27
    @Author  : Bright Hsu
    @Email   : hsubright@163.com
    @FileName: models.py
    @Software: PyCharm
"""


from albumy.extensions import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash


# 存储用户信息模型
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    # 资料
    username = db.Column(db.String(20), unique=True, index=True)
    email = db.Column(db.String(254), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(30))
    website = db.Column(db.String(255))
    bio = db.Column(db.String(120))
    member_since = db.Column(db.DateTime, default=datetime.utcnow)
    # 用户状态
    confirmed = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)
