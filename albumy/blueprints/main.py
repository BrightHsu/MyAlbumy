#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
    @Time    : 2020/6/14 10:43
    @Author  : Bright Hsu
    @Email   : hsubright@163.com
    @FileName: main.py
    @Software: PyCharm
"""


from flask import Blueprint, request, redirect, url_for, flash, send_from_directory
from flask import render_template, current_app
from albumy.utils import redirect_back
from flask_login import login_required
from albumy.decorators import permission_required, confirm_required
from albumy.utils import rename_image, resize_image
import os
from albumy.models import Photo
from albumy.extensions import db


main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    return render_template('main/index.html')


@main_bp.route('/explore')
def explore():
    return render_template('main/explore.html')


@main_bp.route('/upload', methods=['GET', 'POST'])
@login_required  # 登录验证
@confirm_required  # 确定状态验证
@permission_required('UPLOAD')  # 上传权限验证
def upload():
    if request.method == 'POST' and 'file' in request.files:
        f = request.files.get('file')  # 获取图片文件对象
        filename = rename_image(f.filename)  # 生成随即文件名
        # 保存图片
        f.save(os.path.join(current_app.config['ALBUMY_UPLOAD_PATH'], filename))
        filename_s = resize_image(f, filename, current_app.ALBUMY_PHOTO_SIZE['small'])
        filename_m = resize_image(f, filename, current_app.ALBUMY_PHOTO_SIZE['medium'])
        photo = Photo(
            filename=filename,
            filename_s=filename_s,
            filename_m=filename_m,
            author=current_app._get_current_object()
        )
        db.session.add(photo)
        db.session.commit()
    return render_template('main/upload.html')


# 返回头像图片的url
@main_bp.route('/avatars/<path:filename>')
def get_avatar(filename):
    return send_from_directory(current_app.config['AVATARS_SAVE_PATH', filename])