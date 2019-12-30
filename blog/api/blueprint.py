# -*- coding: utf-8 -*-
# https://github.com/KazakovDenis
import os
from flask import Blueprint, redirect, url_for, request, render_template
from models import Post, Tag
from app import db, CONFIG
from flask_security import login_required
from werkzeug.utils import secure_filename


api = Blueprint('api', __name__, template_folder='templates')


@api.route('/')
def index():
    page = request.args.get('page')
    page = int(page) if (page and page.isdigit()) else 1
    q = request.args.get('q')

    if q:
        posts = Post.query.filter(Post.title.contains(q) | Post.body.contains(q))
    else:
        posts = Post.query.order_by(Post.created.desc())

    tags = Tag.query.all()
    result = {post.id: (post.title, post.body, post.tags) for post in posts}

    return result
