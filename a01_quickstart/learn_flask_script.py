#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

from flask import Flask
from flask_script import Manager, Command, Option

app = Flask(__name__)
# configure your app
manager = Manager(app)


class Hello(Command):  # 默认方式添加命令
    """prints hello world"""
    def run(self):
        print("hello world")

manager.add_command('hello', Hello())


class Hello_OPT(Command):  # 添加命令，并未命令添加参数
    def __init__(self, default_name='Xu Weiman'):
        super().__init__()
        self.default_name = default_name

    def get_options(self):
        return [
            Option('-n', '--name', dest='name', default=self.default_name),
        ]

    def run(self, name):
        print("hello",  name)

manager.add_command('hello_opt', Hello_OPT())


@manager.command
def hello_again(words):
    """Just say hello again"""
    print("Hello again,", words)
# python learn_flask_script.py hello_again good_night


@manager.command
def say_word(words='Cool!'):
    print('Hey, %s' % words)
# python learn_flask_script.py say_word good_night  #爆异常
# python learn_flask_script.py say_word -w good_night  #或者 -w=good_night , -w是参数的首字母
# python learn_flask_script.py say_word --words good_night  #或者 --words=good_night


@manager.option('-n', '--name',dest='name', default='xuweiman', help='Your name')  # dest表示option作用在哪个参数
# 如果是多个参数的，可以使用多个manager.option装饰
def say_name(name):
    print("Hello", name)
# python learn_flask_script.py say_name xuweiman #报异常
# python learn_flask_script.py say_name -n xuweiman #或者-n=xuweiman ; --name xuweiman; --name=xuweiman


if __name__ == "__main__":
    manager.run()
