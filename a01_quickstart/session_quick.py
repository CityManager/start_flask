#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
from flask import Flask, session, escape, request, redirect, url_for

__author__ = 'CityManager'

"""
Session 的简单使用，在没有使用jinja2的情况下，需要设置app.secret_key属性
并且在获取session数据时需要使用escape方法来进行解析。
"""

app = Flask(__name__)


@app.route('/')
def index():
    # 如果username在session中，则解析session总username的数据，并放入响应中
    if 'username' in session:
        u_name = escape(session['username'])
        print(type(u_name))
        return 'Logged in as {}'.format(u_name)
    return 'You are not Logged in'


@app.route('/login', methods=['GET', 'POST'])
def login():
    # 如果是POST方法请求则处理表单数据，否则返回表单给用户填写
    if request.method == 'POST':
        # 从表单中获取username数据，并存入session中
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    else:
        return '''
            <form action="" method="post">
                <p><input type=text name=username>
                <p><input type=submit value=Login>
            </form>
        '''


@app.route('/logout')
def logout():
    # 从session中剔除username数据
    session.pop('username')
    return redirect(url_for('index'))


app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


# 自动生成 secret_key 的方法
# os.urandom(24)


if __name__ == '__main__':
    app.debug = True
    app.run()
