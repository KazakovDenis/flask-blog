"""
Module executes functions to start the project and contains functions to manage the project manually
"""
import re
from subprocess import check_call

from blog.models import User, Role, Tag, db, user_datastore
from blog.wsgi import app


log = app.logger


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


def main():
    check = input('Are you sure the database has been created and environment variables are set? [y/n] --> ').lower()
    if check in ['y', 'yes', 'д', 'да']:
        db.create_all()
        db.session.commit()
        log.info('Tables have been created!')

        add_new_role(name='admin', description='A head of project')
        add_new_role(name='subscriber', description='A member of society')
        add_new_user(email='admin@admin.com', password='admin123', role='admin')

        check_call(['flask', 'db', 'init'])
        check_call(['flask', 'db', 'migrate'])
        check_call(['flask', 'db', 'upgrade'])

        tag = Tag(name='projects')
        db.session.add(tag)
        db.session.commit()
        log.info('Now you can test the project by >> flask run')
    else:
        log.info('Aborted.')


if __name__ == '__main__':
    main()
