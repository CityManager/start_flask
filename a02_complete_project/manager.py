#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
import sys
import os
# 添加 入口python文件的上一级目录到path中，便于内部使用相对路径import
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell
from a02_complete_project.flasky import create_app, db
from a02_complete_project.flasky.models import BoardMessage

__author__ = 'CityManager'

app = create_app(os.getenv('FLASK_CONFIG', 'default'))
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, BoardMessage=BoardMessage)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manager.run()
