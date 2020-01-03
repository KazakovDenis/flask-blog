# -*- coding: utf-8 -*-
# https://github.com/KazakovDenis
import os
import sys

from app import app
from flask import render_template, request, url_for, redirect
from models import Post, Tag


@app.route('/hook', methods=['POST', 'GET'])
def hook():
    if request.method == 'POST':
        conditions = (request.headers.get('X-Hub-Signature'),
                      request.data['repository']['id'] == 208764257,
                      request.data['sender']['id'] == 45169520)
        if all(conditions):
            os.execl(sys.executable, 'python', 'deployer.py')
            return 'Successfully', 200
        else:
            return 'Forbidden', 403
    return redirect(url_for('index'))


@app.route('/')
def index():
    posts = Post.query.order_by(Post.created.desc()).all()[:10]
    tags = Tag.query.all()[:50]
    return render_template('index.html', posts=posts, tags=tags)


@app.errorhandler(404)
def page_not_found(event):
    return render_template('404.html'), 404
