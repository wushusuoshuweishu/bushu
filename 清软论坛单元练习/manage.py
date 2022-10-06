# -*- coding: utf-8 -*-
import coverage
import os
from app import create_app
from app import db
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from app.models.model import User
from app.utils import config
import sys
import unittest
from app.utils.jwt import encrypt_password

COV=coverage.coverage(branch=True,include='app/*')
COV.start()
# 设置默认模式
app = create_app(os.getenv('TYPE', 'default'))
host = config.get_yaml('app.HOST')
port = config.get_yaml('app.PORT')

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('runserver', Server(host=host, port=port))
manager.add_command('db', MigrateCommand)

@manager.command
def test(filter=None):
    """Run the unit tests"""
    loader = unittest.TestLoader()
    loader.testNamePatterns = [filter+"*"] if filter is not None else None
    tests = loader.discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    COV.stop()
    COV.save()
    print('Coverage:')
    COV.report()
    basedir = os.path.abspath(os.path.dirname("backend"))
    covdir = os.path.join(basedir, 'test_report')
    COV.html_report(directory=covdir)
    print('HTML version: file://%s/index.html' % covdir)

@manager.command
def init_db():
    """Init db"""
    db.create_all()
    me = User(username="test", password=encrypt_password(str("test")), nickname="test", mobile="+86.123456789012", magic_number=0, url="https://baidu.com") # noqa: E501
    db.session.add(me)
    db.session.commit()

if __name__ == '__main__':
    manager.run()
