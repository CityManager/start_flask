#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
import datetime

from flask import flash, url_for, redirect, render_template, request

from . import main_blueprint
from a02_complete_project.flasky import db
from a02_complete_project.flasky.main.forms import MessageForm
from a02_complete_project.flasky.models import BoardMessage

__author__ = 'CityManager'


@main_blueprint.route('/', methods=['POST', 'GET'])
@main_blueprint.route('/page/', methods=['POST', 'GET'])
@main_blueprint.route('/page/<int:page>', methods=['POST', 'GET'])
def index(page=1):
    form = MessageForm()
    if request.method == "POST":  # 表单请求到达后，获取表单数据，存入数据库
        if form.validate_on_submit():
            message = BoardMessage()
            message.author = form.author.data
            message.subject = form.subject.data
            message.message = form.message.data
            message.create_time = datetime.datetime.utcnow()  # 更新上创建时间
            db.session.add(message)
            db.session.commit()
            flash('Message {} saved successfully!'.format(message.subject))
            return redirect(url_for('main.index'))
    # messages = BoardMessage.query.order_by(BoardMessage.create_time.desc()).all()
    pages = BoardMessage.query.paginate(page, 5, False)
    return render_template('main/index.html', form=form, pages=pages)
