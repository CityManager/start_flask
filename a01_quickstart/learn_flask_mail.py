#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
import getpass
import os
from threading import Thread
from flask import Flask, session, redirect, url_for, render_template, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_script import Manager, Shell
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_mail import Message, Mail

__author__ = 'CityManager'

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'hey hey, you socks'  # 提供给flask-wtf模块实现scr攻击保护
Bootstrap(app)  # 使用flask_bootstrap扩展
Moment(app)
db = SQLAlchemy(app)
manager = Manager(app)

app.config['MAIL_SERVER'] = 'smtp.163.com'
app.config['MAIL_PORT'] = 25
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USERNAME'] = input('请输入邮箱地址:')
app.config['MAIL_PASSWORD'] = getpass.getpass('请输入邮箱密码:')
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flasky]'
app.config['FLASKY_MAIL_SENDER'] = 'weiman_gz@163.com'
mail = Mail(app)


def send_async_email(app, msg):  # 用到app的config数据，需要使用app的上下文
    with app.app_context():
        mail.send(msg)


def send_mail(send_to, subject, template, **kw):  # 使用线程执行邮件发送，避免请求阻塞
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,
                  sender=app.config['MAIL_USERNAME'], recipients=[send_to])
    msg.body = render_template(template + '.txt', **kw)
    msg.html = render_template(template + '.html', **kw)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr


class Role(db.Model):
    __tablename__ = 'roles'  # 定义关联的表名
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(64), unique=True)
    user = db.relationship('User', backref=db.backref('role', lazy='joined'), lazy='dynamic')

    def __repr__(self):
        return '<Role %s>' % self.role_name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))  # 表名.主键

    def __repr__(self):
        return '<User %s>' % self.username


def make_shell_context():  # 为flask-script扩展的shell选项配置可用变量
    return dict(app=app, db=db, User=User, Role=Role)

manager.add_command('shell', Shell(make_context=make_shell_context))


class NameForm(Form):  # 定义表单类
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route('/', methods=['POST', 'GET'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        # 获取表单对象中文本框的数据
        username = form.name.data

        # flask-sqlalchemy扩展查询用法
        user = User.query.filter_by(username=username).first()
        if not user:
            user = User(username=username)
            db.session.add(user)
            db.session.commit()
            flash('Add {} to database'.format(username))  # 发送信息给模板
            # 发送新增用户邮件
            send_mail("740557817@qq.com", '新增用户', 'mail/new_user', username=username)
        if old_name and old_name != user.username:
            flash('Looks like you have changed your name!')

        # 重新将数据放入session中
        session['name'] = user.username
        return redirect(url_for('index'))
    return render_template('use_flask_wtf.html', form=form,  name=session.get('name'))


@app.route('/flask_bootstrap/')
def use_flask_bootstrap():
    return render_template('use_flask_bootstrap.html', name='xuweiman')


if __name__ == '__main__':
    manager.run()