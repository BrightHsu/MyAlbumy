#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
    @Time    : 2020/6/14 10:43
    @Author  : Bright Hsu
    @Email   : hsubright@163.com
    @FileName: main.py
    @Software: PyCharm
"""


from flask import Blueprint
from flask import render_template

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    return render_template('main/index.html')


@main_bp.route('/explore')
def explore():
    return render_template('main/explore.html')
