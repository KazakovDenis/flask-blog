# -*- coding: utf-8 -*-
# https://github.com/KazakovDenis
import os
from flask import Blueprint, redirect, url_for, request, render_template
from ..models import Post, Tag
from .forms import PostForm
from ..app import db, CONFIG
from flask_security import login_required
from werkzeug.utils import secure_filename


# всё, что относится к блюпринтам, находится под адресом /blog
posts = Blueprint('posts', __name__, template_folder='templates')


# проверяем загруженное изображение на соответствие расширению
def _allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in CONFIG.ALLOWED_EXTENSIONS


@posts.route('/upload', methods=['POST', 'GET'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and _allowed_file(file.filename):
            filename = secure_filename(file.filename)   # провекра заливаемого файла на безопасность
            img = os.path.join(CONFIG.UPLOAD_FOLDER, filename)
            file.save(img)
            file.close()
            form = PostForm()   # без формы не рендерится
            return render_template('posts/create_post.html', form=form, img=img)    # продумать, как заменить
    # при попытке get-запроса направляем на главную
    return redirect(url_for('index'))


@posts.route('/<slug>/edit', methods=['POST', 'GET'])
@posts.route('/create', methods=['POST', 'GET'])
@login_required
def create_post(slug=None, img=None):
    # при наличии слага выдаём форму редактирования либо постим изменения
    if slug:
        post = Post.query.filter(Post.slug == slug).first_or_404()
        # вносим изменения в пост
        if request.method == 'POST':
            # в formdata пишем данные формы класса ПостФорм, в obj принимаем значения поста
            form = PostForm(formdata=request.form, obj=post)
            form.populate_obj(post)  # метод заполняет форму данным из аргумента
            db.session.commit()
            return redirect(url_for('posts.post_detail', slug=post.slug))
        # выдаём страницу редактирования
        form = PostForm(obj=post)
        return render_template('posts/create_post.html', post=post, form=form)

    # если слага нет, выдаём пустую форму и постим новую запись
    # пишем пост в БД
    if request.method == 'POST':
        title = request.form['title']  # получаем значение поля title формы
        body = request.form['body']
        try:
            post = Post(title=title, body=body)
            db.session.add(post)
            db.session.commit()
        except Exception as e:
            print(e)
        return redirect(url_for('posts.index'))
    # выдаём страницу создания записи
    form = PostForm()
    return render_template('posts/create_post.html', form=form, img=img)


@posts.route('/')
def index():
    # принимаем аругменты из адресной строки
    # обработчик пагинации
    page = request.args.get('page')

    if page and page.isdigit():
        page = int(page)
    else:
        page = 1

    # обработчик формы поиска
    q = request.args.get('q')

    if q:   # если не пустой запрос, ищем посты с запросом в названии и в теле
        posts = Post.query.filter(Post.title.contains(q) | Post.body.contains(q))
    else:
        # извлекаем из БД все посты в виде списка
        posts = Post.query.order_by(Post.created.desc())
    # пагинатор
    pages = posts.paginate(page=page, per_page=10)   # объект pagination
    tags = Tag.query.all()
    # выводим на экран шаблон с пагинацией
    return render_template('posts/index.html', paginator=pages, tags=tags)


# http://domain.com/blog/first-post
# в <slug> передаётся first-post и далее в post_detail
@posts.route('/<slug>')
def post_detail(slug):
    # отфильтровываем в БД посты, имеющие свойство slug, совпадающее с переданными
    # и берём первый найденный пост (он же единственный, т.к. слаг уникален)
    post = Post.query.filter(Post.slug == slug).first_or_404()
    tags = post.tags
    # создаём список смежных постов для правой панели
    cache = []
    for posts_list in [tag.posts.all() for tag in tags]:
        cache.extend(posts_list)
    adjacent_posts = set(cache)
    # выводим на экран шаблон post_detail
    return render_template('posts/post_detail.html', post=post, tags=tags, right_panel=adjacent_posts)


# http://domain.com/blog/tag/the-tag
@posts.route('/tag/<slug>')
def tag_detail(slug):
    tag = Tag.query.filter(Tag.slug == slug).first_or_404()
    tags = Tag.query.all()
    posts = tag.posts.order_by(Post.created.desc()).all()
    return render_template('posts/tag_detail.html', tag=tag, tags=tags, posts=posts)
