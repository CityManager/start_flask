#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

"""
    应用工程
"""
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from ..config import config

__author__ = 'CityManager'

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()


def create_app(config_name):  # 创建app，并且利用各个扩展初始化app
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)

    from .main import main_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/board')

    return app
