# -*- coding: utf-8 -*-
# https://github.com/KazakovDenis
import os
from flask import Blueprint, redirect, url_for, request, render_template
from markdown import markdown
from models import Post, Tag
from .forms import PostForm
from app import db, Configuration, log
from flask_security import login_required
from werkzeug.utils import secure_filename
from html2text import html2text


# всё, что относится к блюпринтам, находится под адресом /blog
posts = Blueprint('posts', __name__, template_folder='templates')


# проверяем загруженное изображение на соответствие расширению
def _allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in Configuration.ALLOWED_EXTENSIONS


@posts.route('/upload/', methods=['POST', 'GET'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and _allowed_file(file.filename):
            filename = secure_filename(file.filename)   # проверка заливаемого файла на безопасность
            img = os.path.join(Configuration.UPLOAD_FOLDER, filename)
            file.save(img)
            file.close()
            form = PostForm()   # без формы не рендерится
            return render_template('posts/create_post.html', form=form, img=img)    # продумать, как заменить
    # при попытке get-запроса направляем на главную
    return redirect(url_for('index'))


@posts.route('/<slug>/edit/', methods=['POST', 'GET'])
@posts.route('/create/', methods=['POST', 'GET'])
@login_required
def create_post(slug=None):
    post = Post.query.filter(Post.slug == slug).first_or_404() if slug else None

    if request.method == 'POST':
        from werkzeug.datastructures import MultiDict
        data = MultiDict(request.form)
        title = data.get('title')
        body = data['body'] = html2text(data.get('body') or '')

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

    pages = posts.paginate(page=page, per_page=10)   # объект pagination
    tags = Tag.query.all()
    return render_template('posts/index.html', paginator=pages, tags=tags)


@posts.route('/<slug>/')
def post_detail(slug):
    the_post = Post.query.filter(Post.slug == slug).first_or_404()
    tags = the_post.tags
    # создаём список смежных постов для правой панели
    cache = []
    for posts_list in [tag.posts.all() for tag in tags if tag.name != 'projects']:
        posts_list = [post for post in posts_list if post.id != the_post.id]
        cache.extend(posts_list)
    adjacent_posts = set(cache)
    return render_template('posts/post_detail.html', post=the_post, tags=tags, right_panel=adjacent_posts)


@posts.route('/tag/<slug>/')
def tag_detail(slug):
    tag = Tag.query.filter(Tag.slug == slug).first_or_404()
    tags = Tag.query.all()
    posts = tag.posts.order_by(Post.created.desc()).all()
    return render_template('posts/tag_detail.html', tag=tag, tags=tags, posts=posts)
