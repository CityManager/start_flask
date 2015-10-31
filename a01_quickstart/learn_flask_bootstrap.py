#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
from datetime import datetime
from flask import Flask, render_template, session, url_for, redirect, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

__author__ = 'CityManager'

app = Flask(__name__)
Bootstrap(app)  # 使用flask_bootstrap扩展
Moment(app)  # 使用flask-moment扩展
app.config['SECRET_KEY'] = 'hey hey, you socks'  # 提供给flask-wtf模块实现scr攻击保护


@app.route('/flask_bootstrap/')
def use_flask_bootstrap():
    return render_template('use_flask_bootstrap.html', name='xuweiman')


@app.route('/flask_moment/')
def use_flask_moment():
    return render_template('use_flask_moment.html', current_time=datetime.utcnow())


class NameForm(Form):  # 定义表单类， 使用了flask-wtf扩展
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route('/flask_wtf/', methods=['POST', 'GET'])
def use_flask_wtf():
    form = NameForm()
    if form.validate_on_submit():  # 检查form中各个字段是否符合要求
        old_name = session.get('name')
        if old_name and old_name != form.name.data:  # 使用flash发送消息
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        return redirect(url_for('use_flask_wtf'))  # Post/重定向/Get 模式，解决刷新页面时浏览器跳出警告问题
    return render_template('use_flask_wtf.html',form=form,  name=session.get('name'))


if __name__ == '__main__':
    app.run(debug=True)
