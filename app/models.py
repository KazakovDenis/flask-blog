# -*- coding: utf-8 -*-
# https://github.com/KazakovDenis
from app import db
from datetime import datetime
import re
from flask_security import UserMixin, RoleMixin
from transliterate import translit


def slugify(txt):
    if not txt:
        return None
    txt = txt.lower()
    # turn to Latin if Cyrillic is here
    pattern = r'[^\w{IsCyrillic}]'
    if re.search(pattern, txt):
        txt = translit(txt, 'ru', reversed=True)
    # replace all special symbols with dashes
    pattern = r'[^a-z0-9]+'
    slug = re.sub(pattern, '-', txt)
    return slug


# в аргументе ForeignKey адрес
post_tags = db.Table('post_tags',
                     db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
                     db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')))


class Post(db.Model):   # модуль SQLAlchemy автоматом называет таблицу именем класса
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    slug = db.Column(db.String(140), unique=True)
    body = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.now())
    # выстраиваем отношения с классом Tag
    # backref неявно создаёт допольнительное свойство связанному классу
    # lazy='dynamic' позволяет при обращении к экземпляру класса получать объект BaseQuery
    tags = db.relationship('Tag', secondary=post_tags, backref=db.backref('posts', lazy='dynamic'))

    def __init__(self, *args, **kwargs):
        super(Post, self).__init__(*args, **kwargs)
        self.generate_slug()

    def generate_slug(self):
        if self.title:
            self.slug = slugify(self.title)

    def __repr__(self):
        return f'{self.id}.{self.title}'


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    slug = db.Column(db.String(100))

    def __init__(self, *args, **kwargs):
        super(Tag, self).__init__(*args, **kwargs)
        self.slug = slugify(self.name)

    def generate_slug(self):
        if self.name:
            self.slug = slugify(self.name)

    def __repr__(self):
        return f'{self.name}'


### Flask security
roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer, db.ForeignKey('role.id')))
# попробовать ForeignKey('users.id', onupdate="CASCADE", ondelete="CASCADE")


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(255))