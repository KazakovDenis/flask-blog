# -*- coding: utf-8 -*-
# https://github.com/KazakovDenis
from .app import app
from flask import render_template
from .models import Post, Tag


@app.route('/')
def index():
    posts = Post.query.order_by(Post.created.desc()).all()[:10]
    tags = Tag.query.all()[:50]
    return render_template('index.html', posts=posts, tags=tags)


@app.errorhandler(404)
def page_not_found(event):
    return render_template('404.html'), 404
