from datetime import datetime

from linktodapp.extensions import db

# dapp 表
class Dapps(db.Model):
    __tablename__ = 'dapps'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(25),nullable=False)
    email = db.Column(db.String(50),nullable=False)
    des = db.Column(db.String(50),nullable=False)
    full_des = db.Column(db.Text(1000),nullable=False)
    web_url = db.Column(db.Text(500),nullable=False)
    app_url = db.Column(db.Text(255))
    authors = db.Column(db.String(100),nullable=False)
    license = db.Column(db.String(50))
    logo_url = db.Column(db.String(255))
    icon_url = db.Column(db.String(255))
    pro_url = db.Column(db.String(255))
    main_net = db.Column(db.Text)
    facebook_url = db.Column(db.String(100))
    twitter_url = db.Column(db.String(100))
    github_url = db.Column(db.String(100))
    reddit_url = db.Column(db.String(100))
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





