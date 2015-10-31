#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
from flask import Flask, url_for

__author__ = 'CityManager'

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World'


#  variable url routes
@app.route('/user/<username>')
def show_user_profile(username):
    # username is str type
    return 'User {}'.format(username)


@app.route('/post/<int:post_id>')
def show_post(post_id):
    # the variable post_id will be converted into int automatically
    # also can see int, float, path ;  path like the default but accepts slashes
    return 'Post {}'.format(post_id)


@app.route('/projects/')
def projects():
    # url with trailing slash, when you visit /projects
    # the flask will redirect to /projects/ for you
    return 'this is a quickstart project'


@app.route('/about')
def about():
    # url without trailing slash, visit /about/ will occur 404 error
    return 'this is the about page'


# generate the url from flask mapped method name
with app.test_request_context():
    print(url_for('hello_world'))
    print(url_for('show_user_profile', username='xu wei man'))
    print(url_for('show_post', post_id=2))
    print(url_for('projects', next='/'))  # add get request parameters


if __name__ == '__main__':
    # enable to reload Flask object on code changes
    app.debug = True
    app.run()
    # app.run(debug=True)  # also can use this method
