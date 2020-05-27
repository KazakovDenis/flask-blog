# -*- coding: utf-8 -*-
# https://github.com/KazakovDenis
from flask import Blueprint, redirect, url_for, request, render_template
from flask_security import login_required
from html2text import html2text
from markdown import markdown

from app.blog import db, log
from app.models import Post, Tag
from .forms import PostForm


posts = Blueprint('posts', __name__, template_folder='templates')


@posts.route('/<slug>/edit/', methods=['POST', 'GET'])
@posts.route('/create/', methods=['POST', 'GET'])
@login_required
def create_post(slug=None):
    """Is used to create a new post or to edit an existed post
    :param slug: attribute 'slug' of the Post object
    """
    post = Post.query.filter(Post.slug == slug).first_or_404() if slug else None

    if request.method == 'POST':
        from werkzeug.datastructures import MultiDict
        data = MultiDict(request.form)
        title, body = data.get('title'), data.get('body', '')

        if all((title, body)):
            data['body'] = markdown(body)
            try:
                if post:
                    form = PostForm(formdata=data, obj=post)
                    form.populate_obj(post)
                    db.session.commit()
                else:
                    post = Post(title=title, body=body)
                    db.session.add(post)
                    db.session.commit()
                return redirect(url_for('posts.post_detail', slug=post.slug))
            except Exception as e:
                log.error(e)
        return redirect(url_for('posts.index'))

    if post:
        body = html2text(post.body)
        form = PostForm(title=post.title, body=body)
    else:
        form = PostForm()
    return render_template('posts/create_post.html', post=post, form=form)


@posts.route('/')
def index():
    """The app index page handler"""
    # обработчик пагинации
    page = request.args.get('page')
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1

    # обработчик формы поиска
    q = request.args.get('q')
    if q:
        posts = Post.query.filter(Post.title.contains(q) | Post.body.contains(q))
    else:
        posts = Post.query.order_by(Post.created.desc())

    all_tags = Tag.query.all()
    pages = posts.paginate(page=page, per_page=10)   # объект pagination
    return render_template('posts/index.html', paginator=pages, all_tags=all_tags, query=q)


@posts.route('/<slug>/')
def post_detail(slug):
    """The post page handler
    :param slug: attribute 'slug' of the Post object
    """
    the_post = Post.query.filter(Post.slug == slug).first_or_404()
    tags = the_post.tags

    # создаём список смежных постов для правой панели
    cache = []
    for posts_list in [tag.posts.all() for tag in tags if tag.name != 'projects']:
        posts_list = [post for post in posts_list if post.id != the_post.id]
        cache.extend(posts_list)

    adjacent_posts = set(cache)
    all_tags = Tag.query.all()
    return render_template('posts/post_detail.html',
                           post=the_post, tags=tags, all_tags=all_tags, adjacent=adjacent_posts)


@posts.route('/tag/<slug>/')
def tag_detail(slug):
    """The tag page handler
    :param slug: attribute 'slug' of the Tag object
    """
    tag = Tag.query.filter(Tag.slug == slug).first_or_404()
    this_tag_posts = tag.posts.order_by(Post.created.desc()).all()
    all_tags = Tag.query.all()
    return render_template('posts/tag_detail.html', tag=tag, all_tags=all_tags, posts=this_tag_posts)
