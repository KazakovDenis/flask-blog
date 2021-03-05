"""
Module executes functions to start the project and contains functions to manage the project manually
"""
import os
import logging

from flask_migrate import init, migrate, upgrade
from flask_script import Command
from sqlalchemy.exc import IntegrityError

from blog import wsgi
from blog.config import APP_ROOT
from blog.init import load_initial_data
from blog.models import db, user_datastore


logger = logging.getLogger(__name__)


class InitAppCommand(Command):
    """Initialize the project database"""

    migrate_dir = APP_ROOT / 'migrations'

    def run(self):
        os.environ.setdefault('FLASK_APP', wsgi.__file__)
        self.create_tables()
        self.migrate()
        self.create_admin()
        load_initial_data()
        logger.info('The application is ready!')

    @staticmethod
    def create_tables():
        logger.info('Creating tables...')
        db.create_all()
        db.session.commit()
        logger.info('SUCCESSFULLY')

    @staticmethod
    def create_admin():
        logger.info('Creating admin user...')
        try:
            role = user_datastore.create_role(name='admin', description='A head of project')
            user = user_datastore.create_user(email='admin@admin.com', password='admin')
            user_datastore.add_role_to_user(user, role)
            db.session.commit()
            logger.info('SUCCESSFULLY')
        except IntegrityError:
            db.session.rollback()
            logger.warning('Admin role or user already exists.')

    def migrate(self):
        logger.info('Applying migrations...')
        directory = str(self.migrate_dir)

        if not self.migrate_dir.exists():
            init(directory)

        with wsgi.app.app_context():
            migrate(directory, message='initial')
            upgrade(directory)
        logger.info('SUCCESSFULLY')


init_command = InitAppCommand()
