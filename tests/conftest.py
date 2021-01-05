import pytest

from blog.config import Configuration
from blog.factory import create_app
from blog.init import register_blueprints
from blog.models import Tag, db, user_datastore as datastore
from blog.services.sitemap import create_sitemap


@pytest.fixture(scope='session')
def config():
    """Test configuration"""
    class Conf:
        TESTING = True
        SECRET_KEY = 'secret'
        WTF_CSRF_ENABLED = False
        DB_URI = 'sqlite:///:memory:'
        MIGRATE_DIR = 'test_migrations'
        DOMAIN = 'http://test.com'
    return Conf


@pytest.fixture(scope='session')
def app(config):
    """Create and configure an app instance for tests"""
    Configuration.TESTING = config.TESTING
    Configuration.SECRET_KEY = config.SECRET_KEY
    Configuration.WTF_CSRF_ENABLED = config.WTF_CSRF_ENABLED
    Configuration.SQLALCHEMY_DATABASE_URI = config.DB_URI
    test_app = create_app(Configuration, migrations_dir=config.MIGRATE_DIR)

    with test_app.app_context():
        db.create_all()

        tag = Tag(name='projects')
        db.session.add(tag)
        db.session.commit()

        register_blueprints(test_app)
        create_sitemap(test_app, config.DOMAIN)
        yield test_app


@pytest.fixture
def client(app):
    """A test client for the app"""
    with app.test_client() as test_client:
        yield test_client


@pytest.fixture(scope='session')
def credentials():
    """Credentials for the test user"""
    return {'email': 'user@test.com', 'password': 'p@$$w0rd'}


@pytest.fixture(scope='session')
def admin(credentials):
    """Test user"""
    test_user = datastore.create_user(active=True, **credentials)
    test_role = datastore.create_role(name='admin')
    datastore.add_role_to_user(test_user, test_role)
    db.session.commit()
    return test_user
