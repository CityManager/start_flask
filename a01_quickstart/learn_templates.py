#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
from datetime import datetime
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment

__author__ = 'CityManager'

app = Flask(__name__)
Bootstrap(app)  # 使用flask_bootstrap扩展
Moment(app)


@app.route('/micros/')
def learn_micros():
    return render_template('common.html', comments=range(1, 10))


@app.route('/include/')
def learn_include():
    return render_template('base.html', comments=range(1, 10))


@app.route('/extends/')
def learn_extend():
    return render_template('use_base.html', comments=range(1, 10))


@app.route('/flask_bootstrap/')
def use_flask_bootstrap():
    return render_template('use_flask_bootstrap.html', name='xuweiman')


@app.route('/flask_moment/')
def use_flask_moment():
    return render_template('use_flask_moment.html', current_time=datetime.utcnow())


if __name__ == '__main__':
    app.run(debug=True)
