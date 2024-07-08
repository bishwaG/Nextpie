# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask import Flask, url_for
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from importlib import import_module
from logging import basicConfig, DEBUG, getLogger, StreamHandler
from os import path
from app.base.util import hash_pass



from config import Config
app = Flask(__name__, static_folder='base/static')
app.config.from_object(Config)

db = SQLAlchemy()
login_manager = LoginManager()

def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)

def register_blueprints(app):
	for module_name in ('base', 'home', 'api', 'admin'):
		module = import_module('app.{}.routes'.format(module_name))
		app.register_blueprint(module.blueprint)

def configure_database(app):

    @app.before_first_request
    def initialize_database():
        db.create_all()

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()

def create_app(config):

	register_extensions(app)
	register_blueprints(app)
	configure_database(app)
	return app

## Seeding the database
## Manually run 'flask seed'
## database dump
## Manually run 'flask dump --database db.sqlite3 --out nextpiw.sql'
from app.cli import *

