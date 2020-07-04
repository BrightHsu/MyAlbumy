#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
    @Time    : 2020/6/14 10:25
    @Author  : Bright Hsu
    @Email   : hsubright@163.com
    @FileName: settings.py
    @Software: PyCharm
"""


import os
import sys

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

WIN = sys.platform.startswith('win')

if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'


class Operations:
    CONFIRM = 'confirm'
    RESET_PASSWORD = 'reset-password'
    CHANGE_EMAIL = 'change-email'


class BaseConfig:
    SECRET_KEY = os.getenv('SECRET_KEY', 'secret string')

    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 是否追踪数据库对象的修改
    SQLALCHEMY_RECORD_QUERIES = True  # 用于显式地禁用或启用查询记录，查询记录 在调试或测试模式自动启用

    # email 配置
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = ('Albumy', MAIL_USERNAME)

    ALLOWED_IMAGE_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']

    # email 前缀
    ALBUMY_MAIL_SUBJECT_PREFIX = '[Albumy]'
    # 管理员email
    ALBUMY_ADMIN_EMAIL = os.getenv('ALBUMY_ADMIN_EMAIL')

    # 服务器端验证文件上传大小
    MAX_CONTENT_LENGTH = 3 * 1024 * 1024

    # dropzone配置
    DROPZONE_MAX_FILE_SIZE = 3
    DROPZONE_MAX_FILES = 30
    DROPZONE_ALLOWED_FILE_TYPE = 'image'
    DROPZONE_ENABLE_CSRF = True

    # 图片保存路径
    ALBUMY_UPLOAD_PATH = os.path.join(basedir, 'uploads')

    ALBUMY_PHOTO_SIZE = {'small': 400, 'medium': 800}
    ALBUMY_PHOTO_SUFFIX = {
        ALBUMY_PHOTO_SIZE['small']: '_s',   # thumbnail
        ALBUMY_PHOTO_SIZE['medium']: '_m',  # display
    }

    # avatars头像配置
    AVATARS_SAVE_PATH = os.path.join(ALBUMY_UPLOAD_PATH, 'avatars')
    AVATARS_SIZE_TUPLE = (30, 100, 200)     # 头像尺寸设置小/中/大， 3个正方形尺寸


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = prefix + os.path.join(basedir, 'data-dev.db')


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', prefix + os.path.join(basedir, 'data.db'))


class TestingConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}