#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
from contextlib import closing
import sqlite3

from flask import Flask, g, render_template, session, request, flash, url_for, template_rendered
from werkzeug.exceptions import abort
from werkzeug.utils import redirect

__author__ = 'CityManager'

app = Flask(__name__)
app.config.from_object('config_file')
# print(app.config)   # 输出app内所有配置参数


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


def init_db():
    # with closing( a.open( )) as f: do_something
    # -->   f =  a.open( ); try: do_something;  finally: f.close()
    with closing(connect_db()) as db:
        with open('schema.sql', 'r') as f:
            db.cursor().executescript(f.read())
        db.commit()


# 同一让每一个请求获取 数据库连接
# 并在拆除请求时，关闭数据库连接
@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


@app.route('/')
def show_entries():
    cursor = g.db.execute("select title, article from entries order by id desc")
    entries = [dict(title=row[0], article=row[1]) for row in cursor.fetchall()]
    return render_template('show_entries.html', entries=entries)


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute("insert into entries (title, article) values (?, ?)", [request.form['title'], request.form['article']])
    g.db.commit()
    flash("New entry was successfully posted")
    return redirect(url_for('show_entries'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == "POST":
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in')
    flash('You were logged out')
    return redirect(url_for('show_entries'))


@template_rendered.connect_via(app)  # 绑定信号接收器到 template_rendered 信号对象中
def when_template_rendered(sender, template, context, **extra):
    # 每次template渲染完成都会执行下面的语句
    print('Template %s is rendered with %s' % (template.name, context))

if __name__ == '__main__':
    print(app.url_map)
    print(app.instance_path)
    if not app.debug:
        import logging
        from logging.handlers import RotatingFileHandler
        log_file = 'E:\\pyspace\\pyCharm\\start_flask\\a00_tutorial\\log\\tutorial.log'
        file_handler = RotatingFileHandler(log_file, maxBytes=102400, backupCount=3)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'
        ))
        app.logger.addHandler(file_handler)
    app.run()
