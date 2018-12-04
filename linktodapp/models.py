from datetime import datetime
from sqlalchemy.sql.sqltypes import TIMESTAMP
from linktodapp.extensions import db


# dapp 表
class Dapps(db.Model):
    __tablename__ = 'dapps'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(25))
    slug = db.Column(db.String(25))
    email = db.Column(db.String(50))
    tagline = db.Column(db.String(50))
    full_des = db.Column(db.Text(1000))
    web_url = db.Column(db.Text(500))
    app_url = db.Column(db.Text(255))
    authors = db.Column(db.String(255))
    created = db.Column(db.DateTime, default=datetime.utcnow,index=True)
    lastUpdated = db.Column(db.DateTime, default=datetime.utcnow,index=True)
    license = db.Column(db.String(50))
    logo_url = db.Column(db.String(255))
    icon_url = db.Column(db.String(255))
    pro_url = db.Column(db.String(255))
    main_net = db.Column(db.Text(4294000000))
    facebook_url = db.Column(db.String(100))
    twitter_url = db.Column(db.String(100))
    github_url = db.Column(db.String(100))
    reddit_url = db.Column(db.String(100))
    blog_url = db.Column(db.String(100))
    # 关联的键
    status_id = db.Column(db.Integer)
    platform_id = db.Column(db.Integer)
    categeory_id = db.Column(db.Integer)


# tag 表
class Tags(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20),nullable=False,unique=True)

# 平台表
class Platform(db.Model):
    __tablename__ = 'platform'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50),unique=True)

# 分类表
class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50),unique=True)

# dapp所处状态表
class Status(db.Model):
    __tablename__ = 'status'
    id = db.Column(db.Integer,primary_key=True)
    type = db.Column(db.String(20),unique=True)





