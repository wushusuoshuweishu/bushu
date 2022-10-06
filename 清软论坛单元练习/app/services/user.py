# -*- coding: utf-8 -*-
from app.extensions import db
from app.models import User
from sqlalchemy import and_
from app.utils import encrypt_password
import datetime

class UserService():
    def get_user(self, user_id):
        try:
            u = User.query.filter(User.id==user_id).first()
            return u, True
        except Exception as e:
            print(e)
            return "errors", False

    def create_user(self, username, password, nickname, url, mobile, magic_number):
        try:
            pw = encrypt_password(str(password))
            now = datetime.datetime.now()
            u = User(username=username, password=pw,
                nickname=nickname, url=url,
                mobile=mobile, magic_number=magic_number, created=now, updated=now)
            db.session.add(u)
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def get_user_with_pass(self, username, password):
        try:
            pw = encrypt_password(str(password))
            u = User.query.filter(and_(User.username==username, User.password==pw)).first()
            if u is None:
                return "not found", False
            return u, True
        except Exception as e:
            print(e)
            return "errors", False