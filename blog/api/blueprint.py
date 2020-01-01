# -*- coding: utf-8 -*-
# https://github.com/KazakovDenis
import os
from flask import Blueprint, redirect, url_for, request, render_template
from models import Post, Tag
from app import db, CONFIG
from flask_security import login_required
from werkzeug.utils import secure_filename

api = Blueprint('api', __name__, template_folder='templates')
site = 'https://kazakov.ru.net/blog/'

@api.route('/posts')
def get_posts():
    q = request.args.get('q')
    if q:
        posts = Post.query.filter(Post.title.contains(q) | Post.body.contains(q))
    else:
        posts = Post.query.order_by(Post.created.desc())

    result = {'posts': {post.title: {
                           'id': post.id,
                           'body': post.body,
                           'created': post.created,
                           'URL': site + post.slug,
                           'tags': {tag.name: {'tag.id': tag.id, 'URL': site + 'tag/' + tag.slug}
                                    for tag in post.tags},
                       } for post in posts}}
    return result


@api.route('/tags')
def get_tags():
    q = request.args.get('q')
    if q:
        tags = Tag.query.filter(Tag.name.contains(q)).order_by(Tag.name.asc())
    else:
        tags = Tag.query.order_by(Tag.name.asc())

    result = {'tags': {tag.name: {
                           'id': tag.id,
                           'posts': {post.title:
                                         {'id': post.id,
                                          'URL': site + post.slug,
                                          'body': post.body}
                                     for post in tag.posts},
                       } for tag in tags}}
    return result
