from flask import redirect, url_for, request
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.menu import MenuLink
from flask_admin.contrib.sqla import ModelView
from flask_security import current_user

from .config import PUBLIC_DIR
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
    @expose()
    def index(self):
        return self.render('admin.html')


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


class FilesAdminView(AdminMixin, FileAdmin):
    pass


def create_admin(app, db):
    admin = Admin(app, 'Admin panel', url='/admin', index_view=HomeAdminView(), template_mode='bootstrap3')
    admin.add_views(
        PostAdminView(Post, db.session),
        TagAdminView(Tag, db.session),
        UserAdminView(User, db.session),
        RoleAdminView(Role, db.session),
        FilesAdminView(PUBLIC_DIR, name='Files', url='/admin/files/'),
    )
    admin.add_links(
        MenuLink('Back to app', endpoint='main.get_notes'),
    )
    return admin
