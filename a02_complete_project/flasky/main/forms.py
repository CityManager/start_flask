#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
from flask_wtf import Form
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import Length, DataRequired

__author__ = 'CityManager'


class MessageForm(Form):
    author = StringField('昵称', validators=[DataRequired(), Length(max=30)])
    subject = StringField('主题', validators=[DataRequired(), Length(max=100)])
    message = TextAreaField('留言')
    submit = SubmitField('提交')
