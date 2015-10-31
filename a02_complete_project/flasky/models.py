#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

"""
    应用级别上定义模型，便于被各个蓝本使用
"""
import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime
from ..flasky import db

__author__ = 'CityManager'


class BoardMessage(db.Model):
    __tablename__ = 'board_message'
    id = Column(Integer, primary_key=True)
    author = Column(String(30), unique=False, nullable=False)
    subject = Column(String(100), nullable=False)
    message = Column(Text, unique=False)
    create_time = Column(DateTime, default=datetime.datetime.now())  # 似乎是类被加载后，时间就不会便了。。

    def __repr__(self):
        return "<BoardMessage %s:%s>" % (self.author, self.subject)
