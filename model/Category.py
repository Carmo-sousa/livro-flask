# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy

from config import app_active, app_config

config = app_config[app_active]
db = SQLAlchemy(config.APP)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
