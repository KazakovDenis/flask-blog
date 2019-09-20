# -*- coding: utf-8 -*-
# https://github.com/KazakovDenis
from app import user_datastore
from models import *


# пример запроса в базу:
# post1 = Post.query.filter(Post.title.contains('word')).all()
# post2 = Post.query.filter(Post.title=='another word')

def init_tables_from_models():
    db.create_all()
    db.session.commit()


def add_new_role(name='', description=''):
    user_datastore.create_role(name=name, description=description)
    db.session.commit()


def link_role_to_user(user, role):
    user_datastore.add_role_to_user(user, role)
    db.session.commit()


def add_new_user(email='', password='', role='visitor'):
    pattern = r"([\w\.-]+)@([\w\.-]+)(\.[\w\.]+)"   # checks that text is an email
    match = re.fullmatch(pattern, email)
    if match and len(password) >= 5:
        user_datastore.create_user(email=email, password=password)
        db.session.commit()
        user = User.query.filter(User.email == email)
        link_role_to_user(user, role)
    else:
        return "Wrong email, weak password or role doesn't exist"


def get_roles(user=None):     # добавить поиск по id
    return Role.query.filter(Role.users.contains(user)).all()


def get_users(role=None):
    return User.query.filter(Role.roles.contains(role)).all()


# пример: p = Post(title='Some title', body='Some body')
# add_to_db(p)
def add_to_db(obj):
    db.session.add(obj)
    # db.session.add_all([obj1, obj2, obj3])
    db.session.commit()


def main():
    pass


if __name__ == '__main__':
    main()