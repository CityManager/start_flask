#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
import os
import tempfile
import unittest
import tutorial

__author__ = 'CityManager'


# The Testing Skeleton
class TutorialTestCase(unittest.TestCase):
    def setUp(self):
        # 测试用例中的测试方法执行前的初始化操作
        # 1/创建临时文件 用于临时数据库文件
        # 2/关联 待测试应用对象
        # 3/执行 待测试应用对象的额外初始化工作
        self.db_fd, tutorial.app.config['DATABASE'] = tempfile.mkstemp()
        tutorial.app.config['TESTING'] = True
        self.app = tutorial.app.test_client()
        tutorial.init_db()

    def tearDown(self):
        # 测试用例执行结束 结束工作
        # 1/关闭打开的临时文件
        # 2/解除对待测试应用对象的关联
        os.close(self.db_fd)
        os.unlink(tutorial.app.config['DATABASE'])

    # Test Method
    def test_empty_db(self):
        response_v = self.app.get('/')  # 发起get请求
        assert b'No entries here so far' in response_v.data  # data是响应的内容

    # Test Login and Logout
    def login(self, username, password):
        # 发起post请求
        return self.app.post('/login', data=dict(username=username, password=password),
                             follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def test_login_logout(self):
        rv = self.login('admin', 'default')
        assert b'You were logged in' in rv.data
        rv = self.logout()
        assert b'You were logged out' in rv.data
        rv = self.login('adminx', 'default')
        assert b'Invalid username' in rv.data
        rv = self.login('admin', 'defaultx')
        assert b'Invalid password' in rv.data

    # Test Adding Messages
    def test_add_message(self):
        self.login('admin', 'default')
        rv = self.app.post('/add', data=dict(titel='<hello>', article=b'<strong>HTML</strong> allowed here'),
                           follow_redirects=True)
        assert b'No entries here so far' not in rv.data
        assert '&lt;Hello&gt;' in rv.data
        assert b'<strong>HTML</strong> allowed here' in rv.data


if __name__ == "__main__":
    unittest.main()
