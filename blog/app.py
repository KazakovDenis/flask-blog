# -*- coding: utf-8 -*-
# https://github.com/KazakovDenis
from flask import Flask, redirect, url_for, request
from config.config import *
from flask_admin.contrib.fileadmin import FileAdmin
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_admin import Admin, AdminIndexView
from flask_admin.menu import MenuLink
from flask_admin.contrib.sqla import ModelView
from flask_security import SQLAlchemyUserDatastore, Security, current_user
from os import path as op
from werkzeug.middleware.proxy_fix import ProxyFix


app = Flask(__name__)
app.config.from_object(Configuration)
app.wsgi_app = ProxyFix(app.wsgi_app)
log = app.logger
log.filename = f'{PATH}/log/flask/flask.log'
log.level = 20

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


from posts.blueprint import posts
app.register_blueprint(posts, url_prefix='/blog')

from api.blueprint import api
app.register_blueprint(api, url_prefix='/api')

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
    column_list = ('title', 'tags', 'created')
    form_columns = ('title', 'body', 'tags', 'slug', 'created')


class TagAdminView(AdminMixin, BaseModelView):
    form_columns = ('name', 'posts')


class UserAdminView(AdminMixin, ModelView):
    column_list = ('email', 'roles', 'active')
    form_columns = ('email', 'password', 'roles', 'active')


class RoleAdminView(AdminMixin, ModelView):
    pass


class MyFileAdmin(FileAdmin):
    def is_accessible(self):
        return current_user.has_role('admin')


admin = Admin(app, 'Admin panel', url='/admin', index_view=HomeAdminView(), template_mode='bootstrap3')
admin.add_view(PostAdminView(Post, db.session))
admin.add_view(TagAdminView(Tag, db.session))
admin.add_view(UserAdminView(User, db.session))
admin.add_view(RoleAdminView(Role, db.session))
admin.add_view(FileAdmin(op.join(op.dirname(__file__), 'static'), '/static/', name='Files'))
admin.add_link(MenuLink('Back to blog', endpoint='index'))

# -------- Flask security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)
