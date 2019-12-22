# -*- coding: utf-8 -*-
# https://github.com/KazakovDenis
from flask import Flask, redirect, url_for, request
from config.config import CONFIG
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_security import SQLAlchemyUserDatastore, Security, current_user
from werkzeug.middleware.proxy_fix import ProxyFix   # the http-fixer


app = Flask(__name__)
app.config.from_object(CONFIG)   # записываем в свойство config методом from_object конфигурацию
db = SQLAlchemy(app)    # создаём БД для приложения
migrate = Migrate(app, db)   # создаём миграции (записывают в БД изменения структуры БД приложения)
manager = Manager(app)    # создаём менеджера для управления миграциями
manager.add_command('db', MigrateCommand)   # регистрируем команду db для фиксации состояния приложения
app.wsgi_app = ProxyFix(app.wsgi_app)   # http-fixer помогает фласку разобраться с прокси-запросами
# регистрируем блюпринт под адресом /блог
from posts.blueprint import posts    # импорт расположен здесь во избежание зацикливания
app.register_blueprint(posts, url_prefix='/blog')

# ------ Admin panel
from models import *


# ограничиваем права, иначе направляем на вьюху "логин" блюпринта "секьюрити"
class AdminMixin:
    def is_accessible(self):
        return current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        # параметр next определяет ссылку, куда направлялся пользователь
        return redirect(url_for('security.login', next=request.url))


# если происходит изменение данных модели, то необходимо сгенерировать слаг (для редактирования в админке)
class BaseModelView(ModelView):
    def on_model_change(self, form, model, is_created):
        model.generate_slug()
        return super(BaseModelView, self).on_model_change(form, model, is_created)


class AdminView(AdminMixin, ModelView):
    pass


class HomeAdminView(AdminMixin, AdminIndexView):
    pass


class PostAdminView(AdminMixin, BaseModelView):
    form_columns = ['title', 'body', 'tags']


class TagAdminView(AdminMixin, BaseModelView):
    form_columns = ['name', 'posts']


admin = Admin(app, 'Blog admin panel', url='/', index_view=HomeAdminView(name='Home'))
admin.add_view((PostAdminView(Post, db.session)))
admin.add_view((TagAdminView(Tag, db.session)))

# -------- Flask security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)
