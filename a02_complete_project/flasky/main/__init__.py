#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

"""
    利用蓝本进行分大模块开发，在蓝本中进行路由定义，表单对象创建以及业务逻辑实现
    本蓝本是前台展示模块
"""
from flask import Blueprint

__author__ = 'CityManager'


main_blueprint = Blueprint('main', __name__)

from . import errors, views

