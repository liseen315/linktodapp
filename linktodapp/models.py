from datetime import datetime
from sqlalchemy.sql.sqltypes import TIMESTAMP
from linktodapp.extensions import db


tagging = db.Table('tagging',
                   db.Column('dapp_id', db.Integer, db.ForeignKey('dapps.id')),
                   db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
                   )

# dapp 表
class Dapps(db.Model):
    __tablename__ = 'dapps'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50))
    slug = db.Column(db.String(50))
    email = db.Column(db.String(50),nullable=True)
    tagline = db.Column(db.String(50),nullable=True)
    full_des = db.Column(db.Text(1000))
    web_url = db.Column(db.Text(500))
    app_url = db.Column(db.Text(255))
    authors = db.Column(db.String(255))
    created = db.Column(db.DateTime, index=True)
    lastUpdated = db.Column(db.DateTime, index=True)
    license = db.Column(db.String(50))
    logo_url = db.Column(db.String(255))
    icon_url = db.Column(db.String(255))
    pro_url = db.Column(db.String(255),nullable=True)
    main_net = db.Column(db.Text(4294000000))
    facebook_url = db.Column(db.String(255),nullable=True)
    twitter_url = db.Column(db.String(255),nullable=True)
    github_url = db.Column(db.String(255),nullable=True)
    reddit_url = db.Column(db.String(255),nullable=True)
    blog_url = db.Column(db.String(255),nullable=True)
    # 关联的键
    status_id = db.Column(db.Integer)
    platform_id = db.Column(db.Integer)
    categeory_id = db.Column(db.Integer)
    tags = db.relationship('Tag', secondary=tagging, back_populates='dapps')


# tag 表
class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50),nullable=False,unique=True)
    dapps = db.relationship('Dapps', secondary=tagging, back_populates='tags')


# class Tagging(db.Model):
#     __tablename__='tagging'
#     dapp_id = db.Column(db.Integer,primary_key=True)
#     tag_id = db.Column(db.Integer,primary_key=True)

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





