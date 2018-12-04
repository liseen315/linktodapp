import logging
import os
from logging.handlers import RotatingFileHandler

import click
from flask import Flask
from linktodapp.models import Dapps,Tags,Platform,Category,Status
from linktodapp.extensions import db,migrate,toolbar,whooshee
from linktodapp.reptile import getDataFromRank,getDappDetail,getCategories,getTags
from linktodapp.config import config
from multiprocessing.pool import Pool
from functools import partial

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


def getdappsdata(platform,pagenum):
    rankData = getDataFromRank(pagenum, platform)
    for i,itemdata in enumerate(rankData.get('items')):
        dappname = itemdata.get('name').replace(' ','-').rstrip('-').lower()
        dappData = getDappDetail(dappname).get('item')
        print('-getdappsdata--',pagenum,dappname)
        socials = dappData.get('socials')
        for j,socialsItem in enumerate(socials):
            if socialsItem.get('platform') == 'facebook':
                fburl = socialsItem.get('url')
            elif socialsItem.get('platform') == 'twitter':
                twburl = socialsItem.get('url')
            elif socialsItem.get('platform') == 'blog':
                blogburl = socialsItem.get('url')
            elif socialsItem.get('platform') == 'reddit':
                redditburl = socialsItem.get('url')
            elif  socialsItem.get('platform') == 'github':
                githuburl =  socialsItem.get('url')
        dapp = Dapps(
            name = dappData.get('name'),
            email = '',
            tagline = '',
            full_des= dappData.get('description').lstrip(),
            web_url=dappData.get('sites').get('websiteUrl'),
            app_url=dappData.get('sites').get('app_url'),
            authors=','.join(dappData.get('authors')),
            license=dappData.get('license'),
            logo_url=dappData.get('logoUrl'),
            icon_url=dappData.get('iconUrl'),
            pro_url='',
            main_net = ','.join(dappData.get('contractsMainnet')),
            facebook_url=fburl,
            twitter_url=twburl,
            github_url=githuburl,
            reddit_url=redditburl,
            blog_url=blogburl,
            categeory_id=Category.query.filter_by(name=dappData.get('categories')[0]).first().id,
            status_id=Status.query.filter_by(type=dappData.get('status')).first().id,
            platform_id=Platform.query.filter_by(name=dappData.get('platform').lower()).first().id
        )
        db.session.add(dapp)
        db.session.commit()


# 注册命令
def register_commands(app):

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

    # 初始化表
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        if drop:
            click.confirm('This operation will delete the database, do you want to continue?', abort=True)
            db.drop_all()
            click.echo('Drop tables')
        db.create_all()
        forge()
        click.echo('Initialized database.')

    # 抓数据-这里应该启动线程去抓会快一些...
    @app.cli.command()
    @click.option('--platform', default='ethereum',help='get data from statusofdapp api')
    @click.option('--pagenum',prompt='enter pagenum',help='target pagenum')
    def getdapps(platform,pagenum):
        pool = Pool()
        groups = ([x for x in range(1,int(pagenum)+1)])
        pool.map(partial(getdappsdata,platform),groups)
        pool.close()
        pool.join()
        click.echo('Initialized table dapps')







