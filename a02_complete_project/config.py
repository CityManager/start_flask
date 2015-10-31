#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

"""
    配置：在本模块中定义生产/开发/测试环境配置
"""
import os

__author__ = 'CityManager'

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(50)
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 25
    MAIL_USE_TLS = False
    MAIL_SENDER = os.environ.get('MAIL_SENDER') or 'weiman_gz@163.com'
    MAIL_RECEIVERS = ['740557817@qq.com', ]
    MAIL_SUBJECT_PREFIX = '[Flasky]'

    @staticmethod
    def init_app(app):  # 初始化app的类方法，直接空着即可
        pass


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'production_data.sqlite')


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'development_data.sqlite')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'Testing_data.sqlite')

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
