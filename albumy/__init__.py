#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
    @Time    : 2020/6/14 10:24
    @Author  : Bright Hsu
    @Email   : hsubright@163.com
    @FileName: __init__.py.py
    @Software: PyCharm
"""


from flask import Flask
import os
import click
from albumy.settings import config
from albumy.extensions import db, mail, moment, login_manager, bootstrap, csrf
from albumy.blueprints.admin import admin_bp
from albumy.blueprints.ajax import ajax_bp
from albumy.blueprints.auth import auth_bp
from albumy.blueprints.main import main_bp
from albumy.blueprints.user import user_bp
from flask import render_template
from flask_wtf.csrf import CSRFError


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('albumy')
    app.config.from_object(config[config_name])

    register_extensions(app)
    register_blueprints(app)
    register_shell_context(app)
    # register_template_context(app)
    register_errors(app)
    register_commands(app)
    return app


def register_extensions(app):
    db.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    login_manager.init_app(app)
    bootstrap.init_app(app)
    csrf.init_app(app)


def register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(ajax_bp, url_prefix='/ajax')
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(auth_bp, url_prefix='/auth')


def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db)


# def register_template_context(app):
#     @app.context_processor
#     def make_template_context():
#         pass


def register_errors(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/400.html'), 400

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500,html'), 500

    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        return render_template('errors/400.html', description=e.description), 400


def register_commands(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        """Initialize the database."""
        if drop:
            click.confirm('This operation will delete the database, do you want to continue?', abort=True)
            db.drop_all()
            db.create_all()
            click.echo('Drop tables.')
        db.create_all()
        click.echo('Initialized database.')