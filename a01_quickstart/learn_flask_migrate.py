#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
import os
from flask import Flask, render_template, request, url_for, redirect
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String

__author__ = 'CityManager'

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data2.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['DEBUG'] = True

db = SQLAlchemy(app)
manager = Manager(app)
migrate = Migrate(app, db)  # 使用flask-migrate
manager.add_command('db', MigrateCommand)  # 将migrate基础flask-script的sub-magnger注册到manager上


class Member(db.Model):  # 定义一张表
    __tablename__ = 'member'
    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True)
    email = Column(String(64), unique=False)
    phone = Column(Integer, unique=False)

    def __repr__(self):
        return '<Member %s>' % self.name


@app.route('/')
def index():
    members = Member.query.all()
    return render_template('learn_flask_migrate.html', members=members)


@app.route('/add_member/', methods=['POST', 'GET'])
def add_member():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        if name:
            member = Member(name=name, email=email)
            db.session.add(member)
            db.session.commit()
            return redirect(url_for('index'))
    return render_template('learn_flask_migrate_add.html')


if __name__ == '__main__':
    manager.run()





