import logging
import os
from logging.handlers import RotatingFileHandler

import click
from flask import Flask
from linktodapp.models import Dapps,Tags,Platform,Category,Status
from linktodapp.extensions import db,migrate,toolbar,whooshee
from linktodapp.reptile import getDataFromRank,getDappDetail,getCategories,getTags
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
    register_commands(app)
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

# 注册命令
def register_commands(app):
    # 初始化表
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        if drop:
            click.confirm('This operation will delete the database, do you want to continue?', abort=True)
            db.drop_all()
            click.echo('Drop tables')
        db.create_all()
        click.echo('Initialized database.')

    # 抓数据-这里应该启动线程去抓会快一些...
    @app.cli.command()
    @click.option('--platform', default='ethereum',help='get data from statusofdapp api')
    def getdata(platform):
        rankData = getDataFromRank(1,platform)
        for i,itemdata in enumerate(rankData.get('items')):
            dappname = itemdata.get('name').replace(' ','-').rstrip('-').lower()
            dappData = getDappDetail(dappname)
            dapp = Dapps(
                name = dappData.get('item').get('name'),
                email = '',
                des = '',
                full_des= dappData.get('item').get('description'),
                web_url=dappData.get('item').get('sites').get('websiteUrl'),
                app_url=dappData.get('item').get('sites').get('app_url'),
                authors=','.join(dappData.get('item').get('authors')),
                license=dappData.get('item').get('license'),
                logo_url=dappData.get('item').get('logoUrl'),
                icon_url=dappData.get('item').get('iconUrl'),
                pro_url='',
                main_net = ','.join(dappData.get('item').get('contractsMainnet'))
            )
            db.session.add(dapp)
            db.session.commit()
        click.echo('Initialized table dapps')

    # 需要先执行下这个命令
    @app.cli.command()
    def forge():

        def forgeCategory():
            categoryItems = getCategories().get('items')
            for i,item in enumerate(categoryItems):
                cModel = Category(
                    name= item.get('slug')
                )
                db.session.add(cModel)
                db.session.commit()
            click.echo('Initialized table category')

        def forgePlatform():
            platformList = ['ethereum','eos']
            for i,pitem in enumerate(platformList):
                pModel = Platform(
                    name=pitem
                )
                db.session.add(pModel)
                db.session.commit()
            click.echo('Initialized table platform')

        def forgeTags():
            tagItems = getTags().get('items')
            for i,item in enumerate(tagItems):
                tModel = Tags(
                    name=item
                )
                db.session.add(tModel)
                db.session.commit()
            click.echo('Initialized table tags')

        def forgeStatus():
            statusList = ['live','beta','prototype','Work in progress','concept','broken','stealth','abandoned']
            for i,item in enumerate(statusList):
                sModel = Status(
                    type= item
                )
                db.session.add(sModel)
                db.session.commit()
            click.echo('Initialized table status')

        forgeCategory()
        forgePlatform()
        forgeTags()
        forgeStatus()





