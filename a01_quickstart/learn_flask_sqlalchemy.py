#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
import os
from flask import Flask, session, redirect, url_for, render_template, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_script import Manager, Shell
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

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


def make_shell_context():
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
        username = form.name.data
        user = User.query.filter_by(username=username).first()
        if not user:
            user = User(username=username)
            db.session.add(user)
            db.session.commit()
            flash('Add {} to database'.format(username))
        if old_name and old_name != user.username:
            flash('Looks like you have changed your name!')
        session['name'] = user.username
        return redirect(url_for('index'))
    return render_template('use_flask_wtf.html', form=form,  name=session.get('name'))


@app.route('/flask_bootstrap/')
def use_flask_bootstrap():
    return render_template('use_flask_bootstrap.html', name='xuweiman')


if __name__ == '__main__':
    manager.run()