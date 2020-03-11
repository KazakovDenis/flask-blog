from os import path as op

from flask import redirect, url_for, request
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin import Admin, AdminIndexView
from flask_admin.menu import MenuLink
from flask_admin.contrib.sqla import ModelView
from flask_security import current_user

from .blog import app, db
from .models import Post, Tag, User, Role


class AdminMixin:
    def is_accessible(self):
        return current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('security.login', next=request.url))


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


class MyFileAdmin(AdminMixin, FileAdmin):
    pass


admin = Admin(app, 'Admin panel', url='/admin', index_view=HomeAdminView(), template_mode='bootstrap3')
admin.add_view(PostAdminView(Post, db.session))
admin.add_view(TagAdminView(Tag, db.session))
admin.add_view(UserAdminView(User, db.session))
admin.add_view(RoleAdminView(Role, db.session))
admin.add_view(MyFileAdmin(op.join(op.dirname(__file__), 'static'), '/static/', name='Files'))
admin.add_link(MenuLink('Back to app', endpoint='index'))
