import logging
import os
import click
from flask import Flask,jsonify,request
from multiprocessing.pool import Pool
from functools import partial
from logging.handlers import RotatingFileHandler
from linktodapp.apis.v1 import api_v1
from linktodapp.models import Dapps,Tag,Platform,Category,Status
from linktodapp.extensions import db,migrate,toolbar,whooshee,csrf,babel
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
    register_errors(app)
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
    csrf.init_app(app)
    csrf.exempt(api_v1)
    babel.init_app(app)

# 注册蓝本
def register_blueprints(app):
    # app.register_blueprint(api_v1, url_prefix='/api/v1')
    app.register_blueprint(api_v1, url_prefix='/v1', subdomain='api')  # enable subdomain support

# 初始化dapps
def initdapps(platform,pagenum):
    rankData = getDataFromRank(pagenum, platform)

    for i,itemdata in enumerate(rankData.get('items')):
        slug = itemdata.get('slug')
        if getDappDetail(slug) is None:
            continue
        dappData = getDappDetail(slug).get('item')
        print('-initdapps--',pagenum,slug)
        socials = dappData.get('socials')
        fburl = None
        twburl = None
        blogburl = None
        redditburl = None
        githuburl = None
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

        # 做一堆保护
        categorieId = None
        if len(dappData.get('categories')) > 0 :
            categories = Category.query.filter_by(name=dappData.get('categories')[0]).first()
            categorieId = categories.id
            if categories is None:
                categorie = Category(
                    name=dappData.get('categories')[0]
                )
                db.session.add(categorie)
                db.session.commit()

        status = Status.query.filter_by(type=dappData.get('status')).first()
        if status is None:
            statusModel = Status(
                type=dappData.get('status')
            )
            db.session.add(statusModel)
            db.session.commit()

        authors = None
        if dappData.get('authors') is not None:
            authors = ','.join(dappData.get('authors'))

        dapp = Dapps(
            name = dappData.get('name'),
            slug= dappData.get('slug'),
            full_des= dappData.get('description').lstrip(),
            web_url=dappData.get('sites').get('websiteUrl'),
            app_url=dappData.get('sites').get('app_url'),
            authors=authors,
            license=dappData.get('license'),
            logo_url=dappData.get('logoUrl'),
            icon_url=dappData.get('iconUrl'),
            main_net = ','.join(dappData.get('contractsMainnet')),
            created=dappData.get('created'),
            lastUpdated=dappData.get('lastUpdated'),
            facebook_url=fburl,
            twitter_url=twburl,
            github_url=githuburl,
            reddit_url=redditburl,
            blog_url=blogburl,
            categeory_id=categorieId,
            status_id=Status.query.filter_by(type=dappData.get('status')).first().id,
            platform_id=Platform.query.filter_by(name=dappData.get('platform').lower()).first().id
        )
        db.session.add(dapp)
        db.session.commit()

        # 查找dapp的tag是否在表内,不在就添加进去
        targetDapp =  Dapps.query.get_or_404(dapp.id)
        tags = dappData.get('tags')
        for tagName in tags:
            tag = Tag.query.filter_by(name=tagName.lower()).first()
            if tag is None:
                tag = Tag(
                    name=tagName
                )
                db.session.add(tag)
                db.session.commit()
            if tag not in targetDapp.tags:
                targetDapp.tags.append(tag)
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

        # 初始化默认的tag
        def forgeTags():
            tagItems = getTags().get('items')
            for i,item in enumerate(tagItems):
                tModel = Tag(
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

    # 抓数据
    @app.cli.command()
    @click.option('--platform', default='ethereum',prompt='enter platform',help='get data from statusofdapp api default ethereum')
    @click.option('--pagenum',prompt='enter pagenum',help='target pagenum')
    @click.option('--usepool',is_flag=True,prompt='user pool',help='user pool')
    def getdapps(platform,pagenum,usepool):
        if usepool:
            pool = Pool()
            groups = ([x for x in range(1,int(pagenum)+1)])
            pool.map(partial(initdapps,platform),groups)
            pool.close()
            pool.join()
        else:
            initdapps(platform,pagenum)

        click.echo('Initialized table dapps')


# 注册错误
def register_errors(app):
    @app.errorhandler(404)
    def page_not_found(e):
        if request.accept_mimetypes.accept_json and \
                not request.accept_mimetypes.accept_html \
                or request.path.startswith('/api'):
            response = jsonify(code=404, message='The requested URL was not found on the server.')
            response.status_code = 404
            return response

    @app.errorhandler(405)
    def method_not_allowed(e):
        response = jsonify(code=405, message='The method is not allowed for the requested URL.')
        response.status_code = 405
        return response

    @app.errorhandler(500)
    def internal_server_error(e):
        if request.accept_mimetypes.accept_json and \
                not request.accept_mimetypes.accept_html \
                or request.host.startswith('api'):
            response = jsonify(code=500, message='An internal server error occurred.')
            response.status_code = 500
            return response








