# -*- coding: utf-8 -*-
# https://github.com/KazakovDenis
from flask import Blueprint
from flask import render_template
from models import Post, Tag
from flask import request
from .forms import PostForm
from app import db
from flask import redirect
from flask import url_for
from flask_security import login_required


# всё, что относится к блюпринтам, находится под адресом /blog
posts = Blueprint('posts', __name__, template_folder='templates')

# должен располагатьс выше, чтобы фласк не подумал, что это /слаг
@posts.route('/create', methods=['POST', 'GET'])
@login_required
def create_post():
    q = request.args.get('q')

    if request.method == 'POST':
        title = request.form['title']   # получаем значение поля title формы
        body = request.form['body']

        try:
            post = Post(title=title, body=body)
            db.session.add(post)
            db.session.commit()
        except:
            print('Something went wrong')

        # возвращаем метод (вьюху) index блюпринта posts
        return redirect(url_for('posts.index'))

    form = PostForm()
    return render_template('posts/create_post.html', form=form)


@posts.route('/<slug>/edit', methods=['POST', 'GET'])
@login_required
def edit_post(slug):
    # находим пост для редактирования
    post = Post.query.filter(Post.slug == slug).first_or_404()
    if request.method == 'POST':
        # в formdata пишем данные формы класса ПостФорм, в obj принимаем значения поста
        form = PostForm(formdata=request.form, obj=post)
        form.populate_obj(post)    # метод заполняет форму данным из аргумента
        db.session.commit()
        return redirect(url_for('posts.post_detail', slug=post.slug))

    form = PostForm(obj=post)
    return render_template('posts/edit_post.html', post=post, form=form)


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
    # передаём объект pagination в аргумент paginator функции render_template,
    # который далее будет использован в шаблоне блюпринта
    return render_template('posts/index.html', paginator=pages)


# http://domain.com/blog/first-post
# в <slug> передаётся first-post и далее в post_detail
@posts.route('/<slug>')
def post_detail(slug):
    # отфильтровываем в БД посты, имеющие свойство slug, совпадающее с переданными
    # и берём первый найденный пост (он же единственный, т.к. слаг уникален)
    post = Post.query.filter(Post.slug == slug).first_or_404()
    tags = post.tags
    # выводим на экран шаблон post_detail
    return render_template('posts/post_detail.html', post=post, tags=tags)

# <a href="{{ url_for('posts.post_detail', slug=post.slug) }}">
# url_for() - конструктор ссылок Фласка


# http://domain.com/blog/tag/the-tag
@posts.route('/tag/<slug>')
def tag_detail(slug):
    tag = Tag.query.filter(Tag.slug == slug).first_or_404()
    posts = tag.posts.all()
    return render_template('posts/tag_detail.html', tag=tag, posts=posts)
