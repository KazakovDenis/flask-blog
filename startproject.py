"""
Module executes functions to start the project and contains functions to manage the project manually
"""
import os
import re
from subprocess import check_call


from blog.blog import user_datastore, db, log
from blog.config import PATH
from blog.models import User, Role, Tag


def make_dirs():
    """Creates necessary folders"""
    static_folders = ['uploads', 'img']
    static = os.path.join(PATH, 'blog', 'static')
    if not os.path.exists(static):
        os.mkdir(static)

    for folder in static_folders:
        folder_path = os.path.join(static, folder)
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)


def init_tables_from_models():
    """Initializes database tables if not created"""
    db.create_all()
    db.session.commit()
    log.info('Tables have been created!')


def add_new_role(name: str, description: str) -> Role:
    """Creates new role
    :returns Role obj
    """
    role = user_datastore.create_role(name=name, description=description)
    db.session.commit()
    log.info(f'Role "{name}" has been created!')
    return role


def link_role_to_user(user, role):
    """Adds a new role to the user
    :param user: an instance of User obj
    :param role: an instance of Role obj
    """
    user_datastore.add_role_to_user(user, role)
    db.session.commit()
    log.info(f'Role "{role}" has been linked to user "{user}"!')


def add_new_user(email='', password='', role='subscriber'):
    """Adds new user to db"""
    pattern = r"([\w\.-]+)@([\w\.-]+)(\.[\w\.]+)"   # checks that text is an email
    match = re.fullmatch(pattern, email)
    if match and len(password) >= 5:
        user_datastore.create_user(email=email, password=password)
        db.session.commit()
        log.info(f'User "{email}" has been created!')
        user = User.query.filter(User.email == email).first()
        link_role_to_user(user, role)
    else:
        log.warning("Wrong email, weak password or role doesn't exist")


def get_roles(user: User=None):
    """Returns BaseQuery object with roles
    :param user: an instance of User obj
    """
    return Role.query.filter(Role.users.contains(user)).all()


def get_users(role: Role=None):
    """Returns BaseQuery object with users
    :param role: an instance of Role obj
    """
    return User.query.filter(Role.roles.contains(role)).all()


def add_to_db(obj: db.Model):
    """Adds an instance of a model to db
    :param obj: an instance of db.Model
    """
    db.session.add(obj)
    db.session.commit()
    log.info(f'Object "{obj}" has been created!')


def delete_from_db(obj, confirm: str = None):
    """Deletes a record from db
    :param obj: an instance of db.Model
    :param confirm: 'y' to delete without confirmation
    """
    confirm = confirm or input('Are you sure? [y/n] --> ').lower()
    if confirm in ['y', 'yes', 'д', 'да']:
        db.session.delete(obj)
        db.session.commit()
        log.info(f'Object "{obj}" has been deleted!')


def main():
    check = input('Are you sure the database has been created and environment variables are set? [y/n] --> ').lower()
    if check in ['y', 'yes', 'д', 'да']:
        make_dirs()

        init_tables_from_models()
        add_new_role(name='admin', description='A head of project')
        add_new_role(name='subscriber', description='A member of society')
        add_new_user(email='admin@admin.com', password='admin123', role='admin')

        db_manager = ['python3', '-m', 'app.manage', 'db']
        check_call(db_manager + ['init'])
        check_call(db_manager + ['migrate'])
        check_call(db_manager + ['upgrade'])

        tag = Tag(name='projects')
        add_to_db(tag)
        log.info('Now you can test the project by >> python3 -m app.manage runserver')
    else:
        log.info('Aborted.')


if __name__ == '__main__':
    main()
