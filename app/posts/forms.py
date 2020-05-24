# -*- coding: utf-8 -*-
# https://github.com/KazakovDenis
from wtforms import Form, StringField, TextAreaField


class PostForm(Form):
    title = StringField('Название')
    body = TextAreaField('Содержание')
