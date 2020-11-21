from exts import db
from datetime import datetime

class User(db.Model):
    __tablename__   =   'user';
    id              =   db.Column(db.Integer, primary_key=True, autoincrement=True)
    phone           =   db.Column(db.String(11), nullable=False)
    username        =   db.Column(db.String(50), nullable=False)
    password        =   db.Column(db.String(100), nullable=False)
    sex             =   db.Column(db.String(10), nullable=False)
    img             =   db.Column(db.String(255), nullable=False)
    autograph       =   db.Column(db.String(255), server_default="这个人很懒")

class Life(db.Model):
    __tablename__   =   'life'
    id              =   db.Column(db.Integer, primary_key=True, autoincrement=True)
    content         =   db.Column(db.Text, nullable=False)
    img             =   db.Column(db.String(255), nullable=True)
    creat_time      =   db.Column(db.DateTime, default=datetime.now)

    author_id       =   db.Column(db.Integer, db.ForeignKey('user.id'))
    author          =   db.relationship('User', backref=db.backref('life'))

class Comments(db.Model):
    __tablename__   =   'comments'
    id              =   db.Column(db.Integer, primary_key=True, autoincrement=True)
    content         =   db.Column(db.Text, nullable=False)
    creat_time      =   db.Column(db.DateTime, default=datetime.now)

    life_id         =   db.Column(db.Integer, db.ForeignKey('life.id'))
    user_id         =   db.Column(db.Integer, db.ForeignKey('user.id'))
    life            =   db.relationship('Life', backref=db.backref('comments', order_by=id.desc()))
    user            =   db.relationship('User', backref=db.backref('comments'))

class Characters(db.Model):
    __tablename__   =   'characters'
    id              =   db.Column(db.Integer, primary_key=True, autoincrement=True)
    character       =   db.Column(db.String(50), nullable=False)
    rank            =   db.Column(db.String(50), nullable=True)

    user_id         =   db.Column(db.Integer, db.ForeignKey('user.id'))
    user            =   db.relationship('User', backref=db.backref('character_model'))


class Hobby(db.Model):
    __tablename__   =   'hobby'
    id              =   db.Column(db.Integer, primary_key=True, autoincrement=True)
    hobby           =   db.Column(db.String(500), nullable=False)

    user_id         =   db.Column(db.Integer, db.ForeignKey('user.id'))
    user            =   db.relationship('User', backref=db.backref('hobby_model'))

class Friend(db.Model):
    __tablename__   =   'friend'
    id              =   db.Column(db.Integer, primary_key=True, autoincrement=True)
    friend_id       =   db.Column(db.Integer)

    user_id         =   db.Column(db.Integer, db.ForeignKey('user.id'))
    user            =   db.relationship('User', backref=db.backref('friend'))

class Admin(db.Model):
    __tablename__   =   'admin'
    id              =   db.Column(db.Integer, primary_key=True, autoincrement=True)
    username        =   db.Column(db.String(50), nullable=False)
    password        =   db.Column(db.String(100), nullable=False)
