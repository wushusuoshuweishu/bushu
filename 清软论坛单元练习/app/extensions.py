# -*- coding: utf-8 -*-
"""
Flask 扩展
"""
import os
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger

db = SQLAlchemy()
swagger = Swagger()
