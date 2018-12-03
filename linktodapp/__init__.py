import logging
import os
from logging.handlers import RotatingFileHandler

import click
from flask import Flask
from linktodapp.models import Dapps,Tags,Platform,Category,Status
from linktodapp.extensions import db,migrate,toolbar,whooshee
from linktodapp.config import config


basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG','development')

    app = Flask('linktodapp')
    app.config.from_object(config[config_name])

    register_logging(app)
    register_extensions(app)
    register_blueprints(app)
    return app

# 注册log
def register_logging(app):
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler = RotatingFileHandler(os.path.join(basedir, 'logs/bluelog.log'),maxBytes=10 * 1024 * 1024, backupCount=10)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)
    if not app.debug:
        app.logger.addHandler(file_handler)

# 注册拓展
def register_extensions(app):
    db.init_app(app)
    toolbar.init_app(app)
    migrate.init_app(app)
    whooshee.init_app(app)

# 注册蓝本
def register_blueprints(app):
    pass

