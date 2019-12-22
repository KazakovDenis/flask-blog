# -*- coding: utf-8 -*-
# https://github.com/KazakovDenis
"""
Module executes functions to start the project and contains functions to manage the project manually
"""
from app import user_datastore, db
from models import *
import os


def init_tables_from_models():
    db.create_all()
    db.session.commit()
    print(f'Tables have been created!')


def add_new_role(name='', description=''):
    user_datastore.create_role(name=name, description=description)
    db.session.commit()
    print(f'Role "{name}" has been created!')


def link_role_to_user(user, role):
    user_datastore.add_role_to_user(user, role)
    db.session.commit()
    print(f'Role "{role}" has been linked to user "{user}"!')	


def add_new_user(email='', password='', role='subscriber'):
    pattern = r"([\w\.-]+)@([\w\.-]+)(\.[\w\.]+)"   # checks that text is an email
    match = re.fullmatch(pattern, email)
    if match and len(password) >= 5:
        user_datastore.create_user(email=email, password=password)
        db.session.commit()
        print(f'User "{email}" has been created!')
        user = User.query.filter(User.email == email).first()
        link_role_to_user(user, role)
    else:
        return "Wrong email, weak password or role doesn't exist"


def get_roles(user=None):     # добавить поиск по id
    return Role.query.filter(Role.users.contains(user)).all()


def get_users(role=None):
    return User.query.filter(Role.roles.contains(role)).all()


# пример: >>> p = Post(title='Some title', body='Some body')
#         >>> add_to_db(p)
def add_to_db(obj):
    db.session.add(obj)
    # db.session.add_all([obj1, obj2, obj3])
    db.session.commit()
    print(f'Object "{obj}" has been created!')


def delete_from_db(obj):
    confirm = input('Are you sure? [y/n] --> ').lower()
    if confirm == 'y':
        db.session.delete(obj)
        # db.session.add_all([obj1, obj2, obj3])
        db.session.commit()
        print(f'Object "{obj}" has been deleted!')


def main():
    check = input('Are you sure database has been created and config.py has been edited? [y/n] --> ').lower()
    if check == 'y':
        init_tables_from_models()
        add_new_role(name='admin', description='A head of project')
        add_new_role(name='subscriber', description='A member of society')
        add_new_user(email='admin@admin.com', password='admin123', role='admin')
        os.system('python3 manage.py db init')
        os.system('python3 manage.py db migrate')
        os.system('python3 manage.py db upgrade')
        tag = Tag(name='projects')
        add_to_db(tag)
        print('Now you can test the project by >> python3 manage.py runserver')


if __name__ == '__main__':
    main()
