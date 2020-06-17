#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
    @Time    : 2020/6/14 10:28
    @Author  : Bright Hsu
    @Email   : hsubright@163.com
    @FileName: utils.py
    @Software: PyCharm
"""


from flask import redirect, url_for, request
from flask import current_app

from urllib.parse import urljoin, urlparse

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired

from albumy.extensions import db
from albumy.settings import Operations


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


def redirect_back(default='main.index', **kwargs):
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default, **kwargs))


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_IMAGE_EXTENSIONS']


# 生成验证令牌
def generate_token(user, operation, expire_in=None, **kwargs):
    # expire_in 参数用来设置过期时间，默认3600s
    s = Serializer(current_app.config['SECRET_KEY'], expire_in)  # 令牌序列化对象
    data = {'id': user.id, 'operation': operation}
    data.update(**kwargs)
    return s.dumps(data)


# 验证令牌
def validate_token(user, token, operation):
    s = Serializer(current_app.config['SECRET_KEY'])

    try:
        data = s.load(token)
    except (SignatureExpired, BadSignature):
        return False

    if operation != data.get('operation') or user.id != data.get('id'):
        return False

    if operation == Operations.CONFIRM:
        user.confirmed = True
    else:
        return False

    db.session.commit()
    return True
