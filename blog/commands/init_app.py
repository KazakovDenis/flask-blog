"""
Module executes functions to start the project and contains functions to manage the project manually
"""
import os

from flask_migrate import init, migrate, upgrade
from flask_script import Command
from sqlalchemy.exc import IntegrityError

from blog import wsgi
from blog.config import APP_ROOT
from blog.models import Tag, db, user_datastore


class InitAppCommand(Command):
    """Initialize the project database"""

    migrate_dir = APP_ROOT / 'migrations'

    def run(self):
        os.environ.setdefault('FLASK_APP', wsgi.__file__)
        self.create_tables()
        self.migrate()
        self.create_admin()
        self.create_projects_tag()
        print('The application is ready!')

    @staticmethod
    def create_tables():
        print('Creating tables...')
        db.create_all()
        db.session.commit()
        print('SUCCESSFULLY')

    @staticmethod
    def create_admin():
        print('Creating admin user...')
        try:
            role = user_datastore.create_role(name='admin', description='A head of project')
            user = user_datastore.create_user(email='admin@admin.com', password='admin')
            user_datastore.add_role_to_user(user, role)
            db.session.commit()
            print('SUCCESSFULLY')
        except IntegrityError:
            db.session.rollback()
            print('Admin role or user already exists.')

    # FIXME: tag dependency
    @staticmethod
    def create_projects_tag():
        try:
            tag = Tag(name='projects')
            db.session.add(tag)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

    def migrate(self):
        print('Applying migrations...')
        directory = str(self.migrate_dir)

        if not self.migrate_dir.exists():
            init(directory)

        with wsgi.app.app_context():
            migrate(directory, message='initial')
            upgrade(directory)
        print('SUCCESSFULLY')


init_command = InitAppCommand()
